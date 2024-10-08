from typing import Final

__all__ = ["Uninitialized", "UNINITIALIZED"]


class Uninitialized:
    pass


UNINITIALIZED: Final = Uninitialized()
