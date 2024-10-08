from collections.abc import Callable, Iterator
from contextlib import _GeneratorContextManager, contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Protocol

import pytest

from dbnomics_fetcher_toolbox.___formats.mime import MimeFormat


class DummyResponse(BytesResponse):
    def __init__(self, *, resource: Resource[bytes, bytes]) -> None:
        super().__init__(b"dummy content", resource=resource)

    def read(self) -> bytes:
        return self.payload


class DummySource(BaseSource[bytes, bytes]):
    def __init__(self, *, fetch_error: bool = False) -> None:
        self._fetch_error = fetch_error
        self.fetch_was_successful = False

    def fetch(self, *, resource: Resource[bytes, bytes]) -> DummyResponse:
        if self._fetch_error:
            raise ValueError("Dummy fetch error")
        response = DummyResponse(resource=resource)
        self.fetch_was_successful = True
        return response


class MakeTxtResourceFixture(Protocol):
    def __call__(self, resource_id: ResourceId, *, fetch_error: bool = False) -> Resource[bytes, bytes]: ...


@contextmanager
def create_tmp_file(*, dir: Path, source: str | bytes) -> Iterator[Path]:
    with NamedTemporaryFile(dir=dir) as f:
        file_path = Path(f.name)
        if isinstance(source, str):
            file_path.write_text(source, encoding="utf-8")
        elif isinstance(source, bytes):
            file_path.write_bytes(source)
        yield file_path


@pytest.fixture()
def foo_txt() -> Resource[bytes, bytes]:
    return Resource(
        "foo",
        filename="foo.txt",
        format=MimeFormat("text/plain"),
        source=DummySource(),
    )


@pytest.fixture()
def foo_txt_with_error() -> Resource[bytes, bytes]:
    return Resource(
        "foo",
        filename="foo.txt",
        format=MimeFormat("text/plain"),
        source=DummySource(fetch_error=True),
    )


@pytest.fixture()
def make_tmp_file(tmp_path: Path) -> Callable[[str | bytes], _GeneratorContextManager[Path]]:
    def _make_tmp_file(source: str | bytes) -> _GeneratorContextManager[Path]:
        return create_tmp_file(dir=tmp_path, source=source)

    return _make_tmp_file


@pytest.fixture()
def make_txt_resource() -> MakeTxtResourceFixture:
    def _make_txt_resource(resource_id: ResourceId, *, fetch_error: bool = False) -> Resource[bytes, bytes]:
        return Resource(
            resource_id,
            filename=f"{resource_id}.txt",
            format=MimeFormat("text/plain"),
            source=DummySource(fetch_error=fetch_error),
        )

    return _make_txt_resource
