from collections.abc import Iterator, Sequence
from contextlib import contextmanager

@contextmanager
def iterable_subprocess(
    program: Sequence[str], input_chunks: Iterator[bytes], chunk_size: int = 65536
) -> Iterator[Iterator[bytes]]: ...
