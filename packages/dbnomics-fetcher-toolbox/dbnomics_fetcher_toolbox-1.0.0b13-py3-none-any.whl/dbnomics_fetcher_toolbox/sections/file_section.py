from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import daiquiri
from contexttimer import Timer
from humanfriendly.text import generate_slug

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox._internal.reports.download_report_builder import DownloadReportBuilder
from dbnomics_fetcher_toolbox.formatters import format_file_path, format_file_path_with_size
from dbnomics_fetcher_toolbox.helpers.constants import INCREMENTAL_MODE_PREFIX, RESUME_MODE_PREFIX
from dbnomics_fetcher_toolbox.sections.download_section import DownloadSection
from dbnomics_fetcher_toolbox.sections.errors import FileNotWritten
from dbnomics_fetcher_toolbox.sections.skip_reasons import SkipReason
from dbnomics_fetcher_toolbox.types import SectionId, SectionPath

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.helpers.downloader_helper import DownloaderHelper


__all__ = ["FileSection"]


logger = daiquiri.getLogger(__name__)


class FileSection(DownloadSection):
    def __init__(
        self,
        *,
        downloader_helper: "DownloaderHelper",
        fail_fast: bool,
        file: Path | str,
        id: SectionId | str | None,
        keep: bool,
        optional: bool,
        parent_path: SectionPath,
        report_builder: DownloadReportBuilder,
        resume_mode: bool,
        updated_at: datetime | None = None,
    ) -> None:
        if isinstance(file, str):
            file = Path(file)
        if file.is_absolute():
            msg = f"`file` must be a relative path, got {str(file)!r}"
            raise ValueError(msg)
        target_dir = downloader_helper.target_dir
        if not file.is_relative_to(target_dir):
            msg = f"`file` must be relative to the target directory {target_dir!s}, got {str(file)!r}"
            raise ValueError(msg)
        self._relative_file = file.relative_to(target_dir)

        if id is None:
            id = generate_slug(str(file))

        super().__init__(
            downloader_helper=downloader_helper,
            fail_fast=fail_fast,
            id=id,
            parent_path=parent_path,
            report_builder=report_builder,
            resume_mode=resume_mode,
        )

        self._keep = keep
        self._optional = optional
        self._updated_at = updated_at

    def create_file_subsection(
        self,
        file: Path | str,
        *,
        id: str | None = None,
        keep: bool = True,
        optional: bool = False,
        updated_at: datetime | None = None,
    ) -> "FileSection":
        return FileSection(
            downloader_helper=self._downloader_helper,
            fail_fast=self._fail_fast,
            file=file,
            id=id,
            keep=keep,
            optional=optional,
            parent_path=self.path,
            report_builder=self._report_builder,
            resume_mode=self._resume_mode,
            updated_at=updated_at,
        )

    @property
    def debug_dir(self) -> Path:
        return self._debug_dir / self._relative_file.parent

    @property
    def file(self) -> Path:
        return self._target_file if self._keep else self._cache_file

    def set_updated_at(self, updated_at: datetime) -> None:
        self._downloader_helper._update_repo.set_updated_at(self.id, updated_at)  # type: ignore # noqa: SLF001

    @property
    def _cache_file(self) -> Path:
        return self._cache_dir / self._relative_file

    def _get_skip_reason(self) -> SkipReason | None:
        for func in [
            lambda: self._get_skip_reason_for_options(fetcher_helper=self._downloader_helper),
            lambda: self._get_skip_reason_for_resume_mode(),
            lambda: self._get_skip_reason_for_incremental_mode(),
        ]:
            reason = func()
            if reason is not None:
                return reason

        return None

    def _get_skip_reason_for_incremental_mode(self) -> SkipReason | None:
        section_id = self.id

        if not self._downloader_helper.is_incremental:
            return None

        updated_at = self._updated_at
        if updated_at is None:
            return None

        previous_updated_at = self._downloader_helper._update_repo.get_updated_at(section_id)  # type: ignore # noqa: SLF001
        if previous_updated_at is None:
            return None

        if previous_updated_at > updated_at:
            logger.warning(
                "%s Last update date %r of section %r is more recent than the new one %r, ignoring invalid value and processing section",  # noqa: E501
                INCREMENTAL_MODE_PREFIX,
                previous_updated_at.isoformat(),
                section_id,
                updated_at.isoformat(),
            )
            return None

        if updated_at > previous_updated_at:
            logger.debug(
                "%s Processing section %r because the new update date %r is more recent than the last one %r",
                INCREMENTAL_MODE_PREFIX,
                section_id,
                updated_at.isoformat(),
                previous_updated_at.isoformat(),
            )
            return None

        assert updated_at == previous_updated_at
        return SkipReason(
            f"{INCREMENTAL_MODE_PREFIX} Skipping section {section_id!r} because the last update date is the same as the new one: {updated_at.isoformat()}"  # noqa: E501
        )

    def _get_skip_reason_for_resume_mode(self) -> SkipReason | None:
        if self._resume_mode and (resumed_file := self.file).is_file():
            return SkipReason(
                f"{RESUME_MODE_PREFIX} Skipping section {self.id!r} because its file already exists: {format_file_path_with_size(resumed_file)}"  # noqa: E501
            )

        return None

    def _on_exception(self, exc: Exception, *, timer: Timer) -> None:
        logger.exception(
            "Error during file section %r",
            self.id,
            duration=format_timer(timer),
            section=self.path_str,
        )
        self._report_builder.register_file_section_failure(self.id, error=exc, timer=timer)

    def _post_is_skipped(self, *, skip_reason: SkipReason) -> None:
        self._report_builder.register_file_section_skip(self.id, file=self.file, message=skip_reason.message)

    def _post_start(self, *, timer: Timer) -> None:
        logger.info(
            "Finished file section %r",
            self.id,
            duration=format_timer(timer),
            section=self.path_str,
        )
        self._report_builder.register_file_section_success(self.id, timer=timer)

    def _post_yield(self, *, timer: Timer) -> None:  # noqa: ARG002
        if not self.file.is_file():
            error = FileNotWritten(self.file, section=self)
            if self._optional:
                logger.debug(str(error))
            else:
                raise error

    def _pre_start(self) -> None:
        logger.debug(
            "Starting file section %r",
            self.id,
            file=format_file_path(self._relative_file),
            section=self.path_str,
        )
        self._report_builder.register_file_section_start(self.id, file=self.file)

    @property
    def _target_file(self) -> Path:
        return self._downloader_helper.target_dir / self._relative_file
