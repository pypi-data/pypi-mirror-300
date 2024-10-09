from typing import TYPE_CHECKING, Any

from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox._internal.reports.base_report_builder import BaseReportBuilder


class ReportBuilderError(FetcherToolboxError):
    def __init__(self, *, msg: str, report_builder: "BaseReportBuilder[Any]") -> None:
        super().__init__(msg=msg)
        self.report_builder = report_builder


class SectionSkipError(ReportBuilderError):
    def __init__(self, section_id: SectionId, *, reason: str, report_builder: "BaseReportBuilder[Any]") -> None:
        msg = f"Could not skip {section_id=} because: {reason}"
        super().__init__(msg=msg, report_builder=report_builder)
        self.reason = reason
        self.section_id = section_id


class SectionStartNotFound(ReportBuilderError):
    def __init__(self, section_id: SectionId, *, report_builder: "BaseReportBuilder[Any]") -> None:
        msg = f"Section start item was not found for {section_id=}"
        super().__init__(msg=msg, report_builder=report_builder)
        self.section_id = section_id
