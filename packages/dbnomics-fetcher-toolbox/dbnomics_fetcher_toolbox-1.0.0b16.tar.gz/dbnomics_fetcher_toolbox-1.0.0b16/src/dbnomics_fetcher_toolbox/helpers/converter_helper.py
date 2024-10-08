from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, Self, TypeVar

import daiquiri
from dbnomics_data_model.model import DatasetCode, DatasetId, ProviderCode

from dbnomics_fetcher_toolbox._internal.reports.convert_report_builder import ConvertReportBuilder
from dbnomics_fetcher_toolbox.helpers.base_fetcher_helper import BaseFetcherHelper
from dbnomics_fetcher_toolbox.sections.convert_section import ConvertSection
from dbnomics_fetcher_toolbox.sections.dataset_section import DatasetSection
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_data_model.storage import Storage


__all__ = ["ConverterHelper"]


logger = daiquiri.getLogger(__name__)


T = TypeVar("T")


class ConverterHelper(BaseFetcherHelper):
    def __init__(
        self,
        *,
        excluded: list[SectionId] | None = None,
        fail_fast: bool = False,
        provider_code: ProviderCode | str,
        report_file: Path | None = None,
        resume_mode: bool = True,
        selected: list[SectionId] | None = None,
        source_dir: Path,
        target_storage: "Storage",
    ) -> None:
        super().__init__(
            excluded=excluded,
            fail_fast=fail_fast,
            report_file=report_file,
            resume_mode=resume_mode,
            selected=selected,
        )

        self.provider_code = ProviderCode.parse(provider_code)
        self.source_dir = source_dir
        self._storage = target_storage

        self._report_builder = ConvertReportBuilder()

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
            self._log_stats()

    def create_convert_section(self, id: str) -> ConvertSection:
        return ConvertSection(
            converter_helper=self,
            fail_fast=self._fail_fast,
            id=id,
            parent_path=[],
            resume_mode=self._resume_mode,
        )

    def create_dataset_section(self, dataset_code: DatasetCode | str, *, id: str | None = None) -> DatasetSection:
        if isinstance(dataset_code, str):
            dataset_code = DatasetCode.parse(dataset_code)

        dataset_id = DatasetId(self.provider_code, dataset_code)

        return DatasetSection(
            converter_helper=self,
            dataset_id=dataset_id,
            fail_fast=self._fail_fast,
            id=id,
            parent_path=[],
            report_builder=self._report_builder,
            resume_mode=self._resume_mode,
        )

    def _get_report_builder(self) -> ConvertReportBuilder:
        return self._report_builder
