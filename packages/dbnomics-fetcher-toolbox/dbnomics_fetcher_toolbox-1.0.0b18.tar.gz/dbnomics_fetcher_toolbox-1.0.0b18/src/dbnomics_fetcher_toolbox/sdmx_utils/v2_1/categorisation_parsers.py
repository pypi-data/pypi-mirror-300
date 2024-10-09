from collections.abc import Iterator

from lxml.etree import QName, _Element  # type: ignore

from .base_parser import Sdmxv21Parser
from .name_parser import NameParser
from .ref_parser import RefParser

__all__ = ["CategorisationParser", "CategorisationsParser"]


class CategorisationParser(NameParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Categorisation")

    def find_target_ref_parser(self, ref_id: str, *, maintainable_parent_id: str | None = None) -> RefParser | None:
        target_ref_element = self._get_target_ref_element(ref_id, maintainable_parent_id=maintainable_parent_id)
        if target_ref_element is None:
            return None

        return RefParser(target_ref_element, file=self.file)

    @property
    def source_ref_parser(self) -> RefParser:
        source_ref_element = self._source_ref_element
        return RefParser(source_ref_element, file=self.file)

    def _get_target_ref_element(self, ref_id: str, *, maintainable_parent_id: str | None = None) -> _Element | None:
        target_ref_element = self.find(f"./str:Target/Ref[@id='{ref_id}']")
        if target_ref_element is None:
            return None

        if (
            maintainable_parent_id is not None
            and target_ref_element.attrib["maintainableParentID"] != maintainable_parent_id
        ):
            return None

        return target_ref_element

    @property
    def _source_ref_element(self) -> _Element:
        return self.find_one("./str:Source/Ref")


class CategorisationsParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Categorisations")

    def iter_categorisation_parsers(self) -> Iterator[CategorisationParser]:
        for categorisation_elements in self._iter_categorisation_elements():
            yield CategorisationParser(categorisation_elements, file=self.file)

    def _iter_categorisation_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./str:Categorisation")
