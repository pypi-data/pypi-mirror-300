r"""Debugger expression language

This module implements the debugger expression language that is used in the UI
to define probe conditions and metric expressions. The JSON AST is compiled into
Python bytecode.

Full grammar:

    predicate               =>  <direct_predicate> | <arg_predicate> | <value_source>
    direct_predicate        =>  {"<direct_predicate_type>": <predicate>}
    direct_predicate_type   =>  not | isEmpty | isDefined
    value_source            =>  <literal> | <operation>
    literal                 =>  <number> | true | false | "string"
    number                  =>  0 | ([1-9][0-9]*\.[0-9]+)
    identifier              =>  <str.isidentifier>
    arg_predicate           =>  {"<arg_predicate_type>": [<argument_list>]}
    arg_predicate_type      =>  eq | ne | gt | ge | lt | le | any | all | and | or
                                | startsWith | endsWith | contains | matches
    argument_list           =>  <predicate>(,<predicate>)+
    operation               =>  <direct_operation> | <arg_operation>
    direct_opearation       =>  {"<direct_op_type>": <value_source>}
    direct_op_type          =>  len | count | ref
    arg_operation           =>  {"<arg_op_type>": [<argument_list>]}
    arg_op_type             =>  filter | substring | getmember | index
"""  # noqa
from dataclasses import dataclass
from itertools import chain
import re
import sys
from types import FunctionType
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from bytecode import Bytecode
from bytecode import Compare
from bytecode import Instr
from bytecode import Label

from ddtrace.debugging._safety import safe_getitem
from ddtrace.internal.compat import PYTHON_VERSION_INFO as PY
from ddtrace.internal.logger import get_logger


DDASTType = Union[Dict[str, Any], Dict[str, List[Any]], Any]

log = get_logger(__name__)


def _is_identifier(name: str) -> bool:
    return isinstance(name, str) and name.isidentifier()


IN_OPERATOR_INSTR = Instr("COMPARE_OP", Compare.IN) if PY < (3, 9) else Instr("CONTAINS_OP", 0)
NOT_IN_OPERATOR_INSTR = Instr("COMPARE_OP", Compare.NOT_IN) if PY < (3, 9) else Instr("CONTAINS_OP", 1)


def short_circuit_instrs(op: str, label: Label) -> List[Instr]:
    value = "FALSE" if op == "and" else "TRUE"
    if PY >= (3, 12):
        return [Instr("COPY", 1), Instr(f"POP_JUMP_IF_{value}", label), Instr("POP_TOP")]

    return [Instr(f"JUMP_IF_{value}_OR_POP", label)]


def instanceof(value: Any, type_qname: str) -> bool:
    try:
        # Try with a built-in type first
        return isinstance(value, __builtins__[type_qname])  # type: ignore[index]
    except KeyError:
        # Otherwise we expect a fully qualified name
        try:
            for c in object.__getattribute__(type(value), "__mro__"):
                module = object.__getattribute__(c, "__module__")
                qualname = object.__getattribute__(c, "__qualname__")
                if f"{module}.{qualname}" == type_qname:
                    return True
        except AttributeError:
            log.debug("Failed to check instanceof %s for value of type %s", type_qname, type(value))

    return False


class DDCompiler:
    @classmethod
    def __getmember__(cls, o, a):
        return object.__getattribute__(o, a)

    @classmethod
    def __index__(cls, o, i):
        return safe_getitem(o, i)

    @classmethod
    def __ref__(cls, x):
        return x

    def _make_function(self, ast: DDASTType, args: Tuple[str, ...], name: str) -> FunctionType:
        compiled = self._compile_predicate(ast)
        if compiled is None:
            raise ValueError("Invalid predicate: %r" % ast)

        instrs = compiled + [Instr("RETURN_VALUE")]
        if sys.version_info >= (3, 11):
            instrs.insert(0, Instr("RESUME", 0))

        abstract_code = Bytecode(instrs)
        abstract_code.argcount = len(args)
        abstract_code.argnames = args
        abstract_code.name = name

        return FunctionType(abstract_code.to_code(), {}, name, (), None)

    def _make_lambda(self, ast: DDASTType) -> Callable[[Any, Any], Any]:
        return self._make_function(ast, ("_dd_it", "_locals"), "<lambda>")

    def _compile_direct_predicate(self, ast: DDASTType) -> Optional[List[Instr]]:
        # direct_predicate       =>  {"<direct_predicate_type>": <predicate>}
        # direct_predicate_type  =>  not | isEmpty | isDefined
        if not isinstance(ast, dict):
            return None

        _type, arg = next(iter(ast.items()))

        if _type not in {"not", "isEmpty", "isDefined"}:
            return None

        value = self._compile_predicate(arg)
        if value is None:
            raise ValueError("Invalid argument: %r" % arg)

        if _type == "isDefined":
            value.append(Instr("LOAD_FAST", "_locals"))
            value.append(IN_OPERATOR_INSTR)
        else:
            value.append(Instr("UNARY_NOT"))

        return value

    def _compile_arg_predicate(self, ast: DDASTType) -> Optional[List[Instr]]:
        # arg_predicate       =>  {"<arg_predicate_type>": [<argument_list>]}
        # arg_predicate_type  =>  eq | ne | gt | ge | lt | le | any | all | and | or
        #                            | startsWith | endsWith | contains | matches
        if not isinstance(ast, dict):
            return None

        _type, args = next(iter(ast.items()))

        if _type in {"or", "and"}:
            a, b = args
            ca, cb = self._compile_predicate(a), self._compile_predicate(b)
            if ca is None:
                raise ValueError("Invalid argument: %r" % a)
            if cb is None:
                raise ValueError("Invalid argument: %r" % b)

            short_circuit = Label()
            return ca + short_circuit_instrs(_type, short_circuit) + cb + [short_circuit]

        if _type in {"eq", "ge", "gt", "le", "lt", "ne"}:
            a, b = args
            ca, cb = self._compile_predicate(a), self._compile_predicate(b)
            if ca is None:
                raise ValueError("Invalid argument: %r" % a)
            if cb is None:
                raise ValueError("Invalid argument: %r" % b)
            return ca + cb + [Instr("COMPARE_OP", getattr(Compare, _type.upper()))]

        if _type == "contains":
            a, b = args
            ca, cb = self._compile_predicate(a), self._compile_predicate(b)
            if ca is None:
                raise ValueError("Invalid argument: %r" % a)
            if cb is None:
                raise ValueError("Invalid argument: %r" % b)
            return cb + ca + [IN_OPERATOR_INSTR]

        if _type in {"any", "all"}:
            a, b = args
            f = __builtins__[_type]  # type: ignore[index]
            ca, fb = self._compile_predicate(a), self._make_lambda(b)

            if ca is None:
                raise ValueError("Invalid argument: %r" % a)

            return self._call_function(
                lambda i, c, _locals: f(c(_, _locals) for _ in i),
                ca,
                [Instr("LOAD_CONST", fb)],
                [Instr("LOAD_FAST", "_locals")],
            )

        if _type in {"startsWith", "endsWith"}:
            a, b = args
            ca, cb = self._compile_predicate(a), self._compile_predicate(b)
            if ca is None:
                raise ValueError("Invalid argument: %r" % a)
            if cb is None:
                raise ValueError("Invalid argument: %r" % b)
            return self._call_function(getattr(str, _type.lower()), ca, cb)

        if _type == "matches":
            a, b = args
            string, pattern = self._compile_predicate(a), self._compile_predicate(b)
            if string is None:
                raise ValueError("Invalid argument: %r" % a)
            if pattern is None:
                raise ValueError("Invalid argument: %r" % b)
            return self._call_function(lambda p, s: re.match(p, s) is not None, pattern, string)

        return None

    def _compile_direct_operation(self, ast: DDASTType) -> Optional[List[Instr]]:
        # direct_opearation  =>  {"<direct_op_type>": <value_source>}
        # direct_op_type     =>  len | count | ref
        if not isinstance(ast, dict):
            return None

        _type, arg = next(iter(ast.items()))

        if _type in {"len", "count"}:
            value = self._compile_value_source(arg)
            if value is None:
                raise ValueError("Invalid argument: %r" % arg)
            return self._call_function(len, value)

        if _type == "ref":
            if not isinstance(arg, str):
                return None

            if arg == "@it":
                return [Instr("LOAD_FAST", "_dd_it")]

            return [
                Instr("LOAD_FAST", "_locals"),
                Instr("LOAD_CONST", self.__ref__(arg)),
                Instr("BINARY_SUBSCR"),
            ]

        return None

    def _call_function(self, func: Callable, *args: List[Instr]) -> List[Instr]:
        if PY < (3, 11):
            return [Instr("LOAD_CONST", func)] + list(chain(*args)) + [Instr("CALL_FUNCTION", len(args))]
        elif PY >= (3, 12):
            return [Instr("PUSH_NULL"), Instr("LOAD_CONST", func)] + list(chain(*args)) + [Instr("CALL", len(args))]

        # Python 3.11
        return (
            [Instr("PUSH_NULL"), Instr("LOAD_CONST", func)]
            + list(chain(*args))
            + [Instr("PRECALL", len(args)), Instr("CALL", len(args))]
        )

    def _compile_arg_operation(self, ast: DDASTType) -> Optional[List[Instr]]:
        # arg_operation  =>  {"<arg_op_type>": [<argument_list>]}
        # arg_op_type    =>  filter | substring | getmember | index | instanceof
        if not isinstance(ast, dict):
            return None

        _type, args = next(iter(ast.items()))

        if _type not in {"filter", "substring", "getmember", "index", "instanceof"}:
            return None

        if _type == "substring":
            v, a, b = args
            cv, ca, cb = self._compile_predicate(v), self._compile_predicate(a), self._compile_predicate(b)
            if cv is None:
                raise ValueError("Invalid argument: %r" % v)
            if ca is None:
                raise ValueError("Invalid argument: %r" % a)
            if cb is None:
                raise ValueError("Invalid argument: %r" % b)
            return cv + ca + cb + [Instr("BUILD_SLICE", 2), Instr("BINARY_SUBSCR")]

        if _type == "filter":
            a, b = args
            ca, fb = self._compile_predicate(a), self._make_lambda(b)

            if ca is None:
                raise ValueError("Invalid argument: %r" % a)

            return self._call_function(
                lambda i, c, _locals: type(i)(_ for _ in i if c(_, _locals)),
                ca,
                [Instr("LOAD_CONST", fb)],
                [Instr("LOAD_FAST", "_locals")],
            )

        if _type == "getmember":
            v, attr = args
            if not _is_identifier(attr):
                raise ValueError("Invalid identifier: %r" % attr)

            cv = self._compile_predicate(v)
            if not cv:
                return None

            return self._call_function(self.__getmember__, cv, [Instr("LOAD_CONST", attr)])

        if _type == "index":
            v, i = args
            cv = self._compile_predicate(v)
            if not cv:
                return None
            ci = self._compile_predicate(i)
            if not ci:
                return None
            return self._call_function(self.__index__, cv, ci)

        if _type == "instanceof":
            v, t = args
            cv = self._compile_predicate(v)
            if not cv:
                return None
            ct = self._compile_predicate(t)
            if not ct:
                return None
            return self._call_function(instanceof, cv, ct)

        return None

    def _compile_operation(self, ast: DDASTType) -> Optional[List[Instr]]:
        # operation  =>  <direct_operation> | <arg_operation>
        return self._compile_direct_operation(ast) or self._compile_arg_operation(ast)

    def _compile_literal(self, ast: DDASTType) -> Optional[List[Instr]]:
        # literal  =>  <number> | true | false | "string" | null
        if not (isinstance(ast, (str, int, float, bool)) or ast is None):
            return None

        return [Instr("LOAD_CONST", ast)]

    def _compile_value_source(self, ast: DDASTType) -> Optional[List[Instr]]:
        # value_source  =>  <literal> | <operation>
        return self._compile_operation(ast) or self._compile_literal(ast)

    def _compile_predicate(self, ast: DDASTType) -> Optional[List[Instr]]:
        # predicate  =>  <direct_predicate> | <arg_predicate> | <value_source>
        return (
            self._compile_direct_predicate(ast) or self._compile_arg_predicate(ast) or self._compile_value_source(ast)
        )

    def compile(self, ast: DDASTType) -> Callable[[Dict[str, Any]], Any]:
        return self._make_function(ast, ("_locals",), "<expr>")


dd_compile = DDCompiler().compile


class DDExpressionEvaluationError(Exception):
    """Thrown when an error occurs while evaluating a dsl expression."""

    def __init__(self, dsl, e):
        super().__init__('Failed to evaluate expression "%s": %s' % (dsl, str(e)))
        self.dsl = dsl
        self.error = str(e)


def _invalid_expression(_):
    """Forces probes with invalid expression/conditions to never trigger.

    Any signs of invalid conditions in logs is an indication of a problem with
    the expression compiler.
    """
    return None


@dataclass
class DDExpression:
    __compiler__ = dd_compile

    dsl: str
    callable: Callable[[Dict[str, Any]], Any]

    def eval(self, _locals):
        try:
            return self.callable(_locals)
        except Exception as e:
            raise DDExpressionEvaluationError(self.dsl, e) from e

    def __call__(self, _locals):
        return self.eval(_locals)

    @classmethod
    def on_compiler_error(cls, dsl: str, exc: Exception) -> Callable[[Dict[str, Any]], Any]:
        log.error("Cannot compile expression: %s", dsl, exc_info=True)
        return _invalid_expression

    @classmethod
    def compile(cls, expr: Dict[str, Any]) -> "DDExpression":
        ast = expr["json"]
        dsl = expr["dsl"]

        try:
            compiled = cls.__compiler__(ast)
        except Exception as e:
            compiled = cls.on_compiler_error(dsl, e)

        return cls(dsl=dsl, callable=compiled)
