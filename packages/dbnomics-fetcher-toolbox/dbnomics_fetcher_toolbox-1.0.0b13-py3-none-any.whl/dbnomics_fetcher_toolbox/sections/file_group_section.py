from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import daiquiri
from contexttimer import Timer

from dbnomics_fetcher_toolbox._internal.file_utils import move_files
from dbnomics_fetcher_toolbox._internal.formatters import format_csv_values, format_timer
from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size
from dbnomics_fetcher_toolbox.sections.download_section import DownloadSection

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.sections.file_section import FileSection

__all__ = ["FileGroupSection"]


logger = daiquiri.getLogger(__name__)


class FileGroupSection(DownloadSection):
    def create_file_subsection(
        self,
        file: Path | str,
        *,
        id: str | None = None,
        keep: bool = True,
        optional: bool = False,
        updated_at: datetime | None = None,
    ) -> "FileSection":
        from .file_section import FileSection

        file_subsection = FileSection(
            downloader_helper=self._downloader_helper,
            fail_fast=self._fail_fast,
            file=file,
            id=id,
            # force to write the file to the cache dir, then self._move_subsection_files will move all of them
            # to the target dir
            keep=False,
            optional=optional,
            parent_path=self.path,
            report_builder=self._report_builder,
            resume_mode=self._resume_mode,
            updated_at=updated_at,
        )

        if keep:
            self._kept_file_subsections.append(file_subsection)

        return file_subsection

    def _move_subsection_files(self) -> None:
        if not self._kept_file_subsections:
            return

        move_files(
            [
                (
                    file_subsection.file,
                    file_subsection._target_file,  # noqa: SLF001 # type: ignore
                )
                for file_subsection in self._kept_file_subsections
            ]
        )
        logger.debug(
            "Moved files of subsections from cache dir to target dir: %s",
            format_csv_values(
                format_file_path_with_size(file_subsection.file) for file_subsection in self._kept_file_subsections
            ),
            section=self.path_str,
        )

    def _on_exception(self, exc: Exception, *, timer: Timer) -> None:  # noqa: ARG002
        logger.exception(
            "Error during file group section %r",
            self.id,
            duration=format_timer(timer),
            section=self.path_str,
        )

    def _post_start(self, *, timer: Timer) -> None:
        logger.info(
            "Finished file group section %r",
            self.id,
            duration=format_timer(timer),
            section=self.path_str,
        )

    def _post_yield(self, *, timer: Timer) -> None:  # noqa: ARG002
        self._move_subsection_files()

    def _pre_start(self) -> None:
        logger.debug("Starting file group section %r", self.id, section=self.path_str)
