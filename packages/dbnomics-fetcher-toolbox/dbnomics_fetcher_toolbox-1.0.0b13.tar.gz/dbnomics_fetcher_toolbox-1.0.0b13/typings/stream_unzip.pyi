from collections.abc import Iterator
from functools import partial as partial

def stream_unzip(
    zipfile_chunks: Iterator[bytes],
    password: bytes | None = None,
    chunk_size: int = 65536,
    allow_zip64: bool = True,  # noqa: FBT001, FBT002
) -> Iterator[tuple[bytes, int, Iterator[bytes]]]: ...
