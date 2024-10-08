import shutil
from collections.abc import Iterable
from pathlib import Path

import daiquiri
from dbnomics_data_model.file_utils import write_gitignore_all

logger = daiquiri.getLogger(__name__)


def create_directory(directory: Path, *, kind: str, with_gitignore: bool = False) -> None:
    if directory.is_dir():
        logger.debug("Using the existing directory %r as the %s directory", str(directory), kind)
        return
    try:
        directory.mkdir(exist_ok=True, parents=True)
    except OSError as exc:
        from dbnomics_fetcher_toolbox.errors.file_utils import DirectoryCreateError

        raise DirectoryCreateError(directory, kind=kind) from exc

    if with_gitignore:
        write_gitignore_all(directory, exist_ok=True)

    logger.debug("Created %s directory: %r", kind, str(directory))


def is_directory_empty(directory: Path) -> bool:
    return not any(directory.iterdir())


def move_files(file_mapping: Iterable[tuple[Path, Path]]) -> None:
    """Move files transactionally.

    If any file fails to move, rollback by moving the files at their original location.
    """
    moved_files: list[tuple[Path, Path]] = []
    try:
        for src_file, dest_file in file_mapping:
            dest_file.parent.mkdir(exist_ok=True, parents=True)
            shutil.move(src_file, dest_file)
            moved_files.append((src_file, dest_file))
    except Exception:
        logger.exception("Error moving a file, rollback")
        for src_file, dest_file in moved_files:
            if dest_file.is_file():
                shutil.move(dest_file, src_file)
        raise


def replace_all_extensions(file: Path, extensions: list[str]) -> Path:
    return file.with_name(file.name.split(".")[0]).with_suffix("".join(extensions))
