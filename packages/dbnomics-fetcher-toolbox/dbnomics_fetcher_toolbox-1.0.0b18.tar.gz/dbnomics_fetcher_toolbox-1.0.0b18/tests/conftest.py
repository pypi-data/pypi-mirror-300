from collections.abc import Callable, Iterator
from contextlib import _GeneratorContextManager, contextmanager  # type: ignore
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import TypeAlias

import pytest


@contextmanager
def create_tmp_file(*, dir: Path, source: str | bytes) -> Iterator[Path]:
    with NamedTemporaryFile(dir=dir) as f:
        file_path = Path(f.name)
        if isinstance(source, str):
            file_path.write_text(source, encoding="utf-8")
        else:
            file_path.write_bytes(source)
        yield file_path


MakeTmpFile: TypeAlias = Callable[[str | bytes], _GeneratorContextManager[Path]]


@pytest.fixture
def make_tmp_file(tmp_path: Path) -> MakeTmpFile:
    def _make_tmp_file(source: str | bytes) -> _GeneratorContextManager[Path]:
        return create_tmp_file(dir=tmp_path, source=source)

    return _make_tmp_file
