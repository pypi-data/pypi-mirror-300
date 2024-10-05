import typing as t

class PeriodicThread:
    name: str
    ident: int
    interval: float

    def __init__(
        self,
        interval: float,
        target: t.Callable,
        name: t.Optional[str] = None,
        on_shutdown: t.Optional[t.Callable] = None,
    ) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def join(self, timeout: t.Optional[float] = None) -> None: ...
    def awake(self) -> None: ...
    def _atexit(self) -> None: ...
    def _after_fork(self) -> None: ...

periodic_threads: t.Dict[int, PeriodicThread]
