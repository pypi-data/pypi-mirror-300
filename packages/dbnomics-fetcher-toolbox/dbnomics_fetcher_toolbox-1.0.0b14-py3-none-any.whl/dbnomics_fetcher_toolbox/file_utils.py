from collections.abc import Iterator
from pathlib import Path

import daiquiri

__all__ = ["iter_child_directories", "write_chunks"]

logger = daiquiri.getLogger(__name__)


def iter_child_directories(base_dir: Path, *, ignore_hidden: bool = True) -> Iterator[Path]:
    """Iterate over child directories of base_dir."""
    for child in base_dir.iterdir():
        if not child.is_dir():
            continue

        dir_name = child.name
        if ignore_hidden and dir_name.startswith("."):
            continue

        yield child


def write_chunks(chunks: Iterator[bytes], *, output_file: Path) -> int:
    total_bytes_written = 0

    partial_output_file = output_file.with_suffix(f"{output_file.suffix}.part")
    output_file.parent.mkdir(exist_ok=True, parents=True)  # in case output_file == "source-data/datasets/dataset1.xml"

    with partial_output_file.open("wb") as fp:
        while True:
            try:
                chunk = next(chunks)
            except StopIteration:
                break

            total_bytes_written += fp.write(chunk)

    partial_output_file.replace(output_file)

    return total_bytes_written
