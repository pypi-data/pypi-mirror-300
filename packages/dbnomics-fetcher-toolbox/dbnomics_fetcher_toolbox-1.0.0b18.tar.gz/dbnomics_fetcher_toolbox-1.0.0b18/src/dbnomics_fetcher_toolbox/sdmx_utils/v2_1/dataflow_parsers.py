from collections.abc import Iterator

from lxml.etree import QName, _Element  # type: ignore

from .base_parser import Sdmxv21Parser
from .errors import DataflowNotFound
from .name_parser import NameParser

__all__ = ["DataflowParser", "DataflowsParser"]


class DataflowParser(NameParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Dataflow")

    @property
    def agency_id(self) -> str:
        return self.element.attrib["agencyID"]

    @property
    def data_structure_id(self) -> str:
        ref_element = self.find_one("./str:Structure/Ref")
        return ref_element.attrib["id"]


class DataflowsParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Dataflows")

    def create_dataflow_parser(self, dataflow_id: str) -> DataflowParser:
        dataflow_element = self._get_dataflow_element(dataflow_id)
        return DataflowParser(dataflow_element, file=self.file)

    def iter_dataflow_parsers(self) -> Iterator[DataflowParser]:
        for dataflow_element in self._iter_dataflow_elements():
            yield DataflowParser(dataflow_element, file=self.file)

    def _get_dataflow_element(self, dataflow_id: str) -> _Element:
        try:
            return self.find_one(f"./str:Dataflow[@id='{dataflow_id}']")
        except ValueError as exc:
            raise DataflowNotFound(dataflow_id, element=self.element) from exc

    def _iter_dataflow_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./str:Dataflow")
