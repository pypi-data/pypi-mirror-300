from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Self

import daiquiri
from contexttimer import Timer

from dbnomics_fetcher_toolbox._internal.reports.download_report_builder import DownloadReportBuilder
from dbnomics_fetcher_toolbox.sections.section import Section
from dbnomics_fetcher_toolbox.sections.skip_reasons import SkipReason
from dbnomics_fetcher_toolbox.types import SectionId, SectionPath

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.helpers.downloader_helper import DownloaderHelper
    from dbnomics_fetcher_toolbox.sections.file_section import FileSection


__all__ = ["DownloadSection"]


logger = daiquiri.getLogger(__name__)


class DownloadSection(Section):
    def __init__(
        self,
        *,
        downloader_helper: "DownloaderHelper",
        fail_fast: bool,
        id: SectionId | str,
        parent_path: SectionPath,
        report_builder: DownloadReportBuilder,
        resume_mode: bool,
    ) -> None:
        super().__init__(fail_fast=fail_fast, id=id, parent_path=parent_path, resume_mode=resume_mode)

        self._downloader_helper = downloader_helper
        self._report_builder = report_builder

        self._kept_file_subsections: list[FileSection] = []

    @contextmanager
    def start(self) -> Iterator[Self]:
        self._pre_start()

        with Timer() as timer:
            try:
                yield self
                self._post_yield(timer=timer)
            except Exception as exc:
                if self._fail_fast:
                    raise
                self._on_exception(exc, timer=timer)
                return

            self._post_start(timer=timer)

    @property
    def _cache_dir(self) -> Path:
        return self._downloader_helper._cache_dir  # noqa: SLF001 # type: ignore[reportPrivateUsage]

    @property
    def _debug_dir(self) -> Path:
        return self._downloader_helper.debug_dir  # type: ignore[reportPrivateUsage]

    def _get_skip_reason(self) -> SkipReason | None:
        return self._get_skip_reason_for_options(fetcher_helper=self._downloader_helper)

    def _on_exception(self, exc: Exception, *, timer: Timer) -> None:
        pass

    def _post_start(self, *, timer: Timer) -> None:
        pass

    def _post_yield(self, *, timer: Timer) -> None:
        pass

    def _pre_start(self) -> None:
        pass
