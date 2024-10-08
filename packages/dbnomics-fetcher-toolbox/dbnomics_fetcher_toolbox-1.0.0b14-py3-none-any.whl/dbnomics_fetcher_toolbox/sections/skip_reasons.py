from dataclasses import KW_ONLY, dataclass

__all__ = ["SkipReason"]


@dataclass
class SkipReason:
    message: str

    _: KW_ONLY
    log_message: bool = True
