from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeVar

from dbnomics_data_model.json_utils import create_default_dumper, dump_as_json_data, save_json_file
from typedload.datadumper import Dumper

from dbnomics_fetcher_toolbox._internal.reports.error_chain import build_error_chain
from dbnomics_fetcher_toolbox._internal.reports.errors import SectionSkipError, SectionStartNotFound
from dbnomics_fetcher_toolbox._internal.typedload_utils import add_handler
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox._internal.reports.convert_report_builder import ConvertReport
    from dbnomics_fetcher_toolbox._internal.reports.download_report_builder import DownloadReport
    from dbnomics_fetcher_toolbox._internal.reports.types import BaseSectionStart


T = TypeVar("T", bound="BaseSectionStart")


class BaseReportBuilder(Generic[T]):
    def __init__(self) -> None:
        self._dumper = self._create_dumper()
        self._section_starts: list[T] = []

    @abstractmethod
    def get_report(self) -> "ConvertReport | DownloadReport": ...

    def save_report(self, output_file: Path) -> None:
        report = self.get_report()
        report_data = dump_as_json_data(report, dumper=self._dumper)
        save_json_file(output_file, report_data)

    def _check_not_already_started(self, section_id: SectionId) -> None:
        if self._find_section_start(section_id) is not None:
            raise SectionSkipError(section_id, reason="Section already started", report_builder=self)

    def _create_dumper(self) -> Dumper:
        dumper = create_default_dumper()
        dumper.strconstructed.add(SectionId)  # type: ignore[reportUnknownMemberType]
        add_handler(
            dumper,
            (
                lambda x: isinstance(x, BaseException),
                lambda _dumper, value, _value_type: build_error_chain(value),
            ),
            sample_value=Exception("sample"),
        )
        return dumper

    def _find_section_start(self, section_id: SectionId) -> T | None:
        for section_start in self._section_starts:
            if section_start.section_id == section_id:
                return section_start

        return None

    def _get_section_start(self, section_id: SectionId) -> T:
        section_start = self._find_section_start(section_id)
        if section_start is None:
            raise SectionStartNotFound(section_id, report_builder=self)

        return section_start
