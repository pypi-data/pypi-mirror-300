from typing import TYPE_CHECKING

import daiquiri
from contexttimer import Timer
from dbnomics_data_model.model import DatasetCode, DatasetId
from dbnomics_data_model.storage import StorageSession
from humanfriendly.text import generate_slug

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox._internal.reports.convert_report_builder import ConvertReportBuilder
from dbnomics_fetcher_toolbox.helpers.constants import RESUME_MODE_PREFIX
from dbnomics_fetcher_toolbox.sections.convert_section import ConvertSection
from dbnomics_fetcher_toolbox.sections.errors import DatasetNotSaved
from dbnomics_fetcher_toolbox.sections.skip_reasons import SkipReason
from dbnomics_fetcher_toolbox.types import SectionId, SectionPath

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.helpers.converter_helper import ConverterHelper


__all__ = ["DatasetSection"]


logger = daiquiri.getLogger(__name__)


class DatasetSection(ConvertSection):
    def __init__(
        self,
        *,
        converter_helper: "ConverterHelper",
        dataset_id: DatasetId,
        fail_fast: bool,
        id: SectionId | str | None,
        parent_path: SectionPath,
        report_builder: ConvertReportBuilder,
        resume_mode: bool,
    ) -> None:
        if id is None:
            id = generate_slug(str(dataset_id.dataset_code))

        super().__init__(
            converter_helper=converter_helper,
            fail_fast=fail_fast,
            id=id,
            parent_path=parent_path,
            resume_mode=resume_mode,
        )

        self.dataset_id = dataset_id
        self._report_builder = report_builder

    @property
    def dataset_code(self) -> DatasetCode:
        return self.dataset_id.dataset_code

    def _get_skip_reason(self) -> SkipReason | None:
        for func in [
            lambda: self._get_skip_reason_for_options(fetcher_helper=self._converter_helper),
            lambda: self._get_skip_reason_for_resume_mode(),
        ]:
            reason = func()
            if reason is not None:
                return reason

        return None

    def _get_skip_reason_for_resume_mode(self) -> SkipReason | None:
        dataset_id = self.dataset_id
        section_id = self.id
        if self._resume_mode and self._converter_helper._storage.has_dataset(dataset_id):  # type: ignore # noqa: SLF001
            return SkipReason(
                f"{RESUME_MODE_PREFIX} Skipping section {section_id!r} because its dataset {dataset_id!r} already exists"  # noqa: E501
            )

        return None

    def _on_exception(self, exc: Exception, *, timer: Timer) -> None:
        logger.exception(
            "Error during dataset section %r",
            self.id,
            duration=format_timer(timer),
            section=self.path_str,
        )
        self._report_builder.register_dataset_section_failure(self.id, error=exc, timer=timer)

    def _post_is_skipped(self, *, skip_reason: SkipReason) -> None:
        self._report_builder.register_dataset_section_skip(
            self.id, dataset_code=self.dataset_code, message=skip_reason.message
        )

    def _post_start(self, *, timer: Timer) -> None:
        logger.debug(
            "Finished dataset section %r",
            self.id,
            duration=format_timer(timer),
            section=self.path_str,
        )
        self._report_builder.register_dataset_section_success(self.id, timer=timer)

    def _post_yield(self, session: StorageSession, *, timer: Timer) -> None:  # noqa: ARG002
        dataset_id = self.dataset_id
        if not session.storage.has_dataset(dataset_id):
            raise DatasetNotSaved(dataset_id, section=self, session=session)

    def _pre_start(self) -> None:
        logger.debug("Starting dataset section %r", self.id, section=self.path_str)
        self._report_builder.register_dataset_section_start(self.id, dataset_code=self.dataset_code)
