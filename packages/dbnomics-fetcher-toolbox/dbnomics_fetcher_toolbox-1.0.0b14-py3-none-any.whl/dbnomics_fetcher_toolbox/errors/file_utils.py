from pathlib import Path

from .base import FetcherToolboxError


class DirectoryCreateError(FetcherToolboxError):
    def __init__(self, directory: Path, *, kind: str) -> None:
        msg = f"Could not create the {kind} directory {str(directory)!r}"
        super().__init__(msg=msg)
        self.directory = directory
        self.kind = kind
