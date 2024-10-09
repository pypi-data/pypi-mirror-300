from types import TracebackType
from typing import Self

class Timer:
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> None: ...
    @property
    def elapsed(self) -> float: ...
