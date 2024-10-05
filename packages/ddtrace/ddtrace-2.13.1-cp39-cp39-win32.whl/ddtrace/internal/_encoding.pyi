from typing import Any
from typing import List
from typing import Optional
from typing import Union
from typing import Tuple

from ddtrace._trace.span import Span

Trace = List[Span]

class ListStringTable(object):
    def index(self, string: str) -> int: ...

class BufferFull(Exception):
    pass

class BufferItemTooLarge(Exception):
    pass

class BufferedEncoder(object):
    max_size: int
    max_item_size: int
    def __init__(self, max_size: int, max_item_size: int) -> None: ...
    def __len__(self) -> int: ...
    def put(self, item: Any) -> None: ...
    def encode(self) -> Tuple[Optional[bytes], int]: ...
    @property
    def size(self) -> int: ...

class ListBufferedEncoder(BufferedEncoder):
    def get(self) -> List[bytes]: ...
    def encode_item(self, item: Any) -> bytes: ...

class MsgpackEncoderBase(BufferedEncoder):
    content_type: str
    def get_bytes(self) -> bytes: ...
    def _decode(self, data: Union[str, bytes]) -> Any: ...

class MsgpackEncoderV03(MsgpackEncoderBase): ...
class MsgpackEncoderV05(MsgpackEncoderBase): ...

def packb(o: Any, **kwargs) -> bytes: ...
