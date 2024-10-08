from collections.abc import Iterator
from datetime import datetime
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, Final, Self, TypeVar

import daiquiri

from dbnomics_fetcher_toolbox._internal.file_utils import create_directory
from dbnomics_fetcher_toolbox._internal.reports import DownloadReportBuilder
from dbnomics_fetcher_toolbox.helpers.base_fetcher_helper import BaseFetcherHelper
from dbnomics_fetcher_toolbox.helpers.update_repo import UpdateRepo

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.sections.file_group_section import FileGroupSection
    from dbnomics_fetcher_toolbox.sections.file_section import FileSection
    from dbnomics_fetcher_toolbox.types import SectionId

__all__ = ["DownloaderHelper"]


logger = daiquiri.getLogger(__name__)


DEFAULT_CACHE_DIR_NAME: Final = "_cache"
DEFAULT_DEBUG_DIR_NAME: Final = "_debug"
DEFAULT_STATE_DIR_NAME: Final = "_state"

T = TypeVar("T")


class DownloaderHelper(BaseFetcherHelper):
    def __init__(
        self,
        *,
        cache_dir: Path | None = None,
        debug_dir: Path | None = None,
        excluded: list["SectionId"] | None = None,
        fail_fast: bool = False,
        is_incremental: bool = True,
        report_file: Path | None = None,
        resume_mode: bool = True,
        selected: list["SectionId"] | None = None,
        state_dir: Path | None = None,
        target_dir: Path,
    ) -> None:
        super().__init__(
            excluded=excluded,
            fail_fast=fail_fast,
            report_file=report_file,
            resume_mode=resume_mode,
            selected=selected,
        )

        if cache_dir is None:
            cache_dir = target_dir / Path(DEFAULT_CACHE_DIR_NAME)
        self._cache_dir = cache_dir

        if debug_dir is None:
            debug_dir = target_dir / Path(DEFAULT_DEBUG_DIR_NAME)
        self.debug_dir = debug_dir

        self.is_incremental = is_incremental

        if state_dir is None:
            state_dir = target_dir / Path(DEFAULT_STATE_DIR_NAME)
        self._state_dir = state_dir

        self.target_dir = target_dir

        self._report_builder = DownloadReportBuilder()
        self._update_repo = UpdateRepo(base_dir=self._state_dir)

        self._create_directories()
        self._update_repo.load()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is None:
            self._log_unmatched_filters()
            self._save_report()
            self._update_repo.save()
            self._log_stats()

    def create_file_section(
        self,
        file: Path | str,
        *,
        id: str | None = None,
        keep: bool = True,
        optional: bool = False,
        updated_at: datetime | None = None,
    ) -> "FileSection":
        from dbnomics_fetcher_toolbox.sections.file_section import FileSection

        return FileSection(
            downloader_helper=self,
            fail_fast=self._fail_fast,
            file=file,
            id=id,
            keep=keep,
            optional=optional,
            parent_path=[],
            report_builder=self._report_builder,
            resume_mode=self._resume_mode,
            updated_at=updated_at,
        )

    def create_file_group_section(self, id: str) -> "FileGroupSection":
        from dbnomics_fetcher_toolbox.sections.file_group_section import FileGroupSection

        return FileGroupSection(
            downloader_helper=self,
            fail_fast=self._fail_fast,
            id=id,
            parent_path=[],
            report_builder=self._report_builder,
            resume_mode=self._resume_mode,
        )

    def iter_selected_section_ids(self) -> Iterator["SectionId"]:
        selected = self._selected
        if selected is not None:
            yield from selected

    def _create_directories(self) -> None:
        create_directory(self._cache_dir, kind="cache", with_gitignore=True)
        create_directory(self.debug_dir, kind="debug", with_gitignore=True)
        create_directory(self._state_dir, kind="state", with_gitignore=True)
        create_directory(self.target_dir, kind="target")

    def _get_report_builder(self) -> DownloadReportBuilder:
        return self._report_builder
