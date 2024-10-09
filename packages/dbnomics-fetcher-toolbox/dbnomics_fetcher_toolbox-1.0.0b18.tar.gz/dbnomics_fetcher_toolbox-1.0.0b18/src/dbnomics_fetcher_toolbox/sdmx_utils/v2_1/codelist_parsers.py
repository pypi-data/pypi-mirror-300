from collections.abc import Iterator

from lxml.etree import QName, _Element  # type: ignore

from .base_parser import Sdmxv21Parser
from .errors import CodelistNotFound
from .name_parser import NameParser

__all__ = ["CodelistParser", "CodelistsParser"]


class CodelistsParser(Sdmxv21Parser):
    def __post_init__(self) -> None:
        self._codelist_element_by_id: dict[str, _Element] = {}

    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Codelists")

    def create_codelist_parser(self, codelist_id: str) -> "CodelistParser":
        codelist_element = self._get_codelist_element(codelist_id)
        return CodelistParser(codelist_element, file=self.file)

    def _get_codelist_element(self, codelist_id: str) -> _Element:
        codelist_element = self._codelist_element_by_id.get(codelist_id)
        if codelist_element is not None:
            return codelist_element

        try:
            codelist_element = self.find_one(f'./str:Codelist[@id="{codelist_id}"]')
        except ValueError as exc:
            raise CodelistNotFound(codelist_id, element=self.element) from exc

        self._codelist_element_by_id[codelist_id] = codelist_element
        return codelist_element


class CodelistParser(NameParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Codelist")

    def create_code_parser(self, code_id: str) -> "CodeParser":
        code_element = self._get_code_element(code_id)
        return CodeParser(code_element, file=self.file)

    def iter_code_parsers(self) -> Iterator["CodeParser"]:
        for code_element in self._iter_code_elements():
            yield CodeParser(code_element, file=self.file)

    def _get_code_element(self, code_id: str) -> _Element:
        return self.find_one(f'./str:Code[@id="{code_id}"]')

    def _iter_code_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./str:Code")


class CodeParser(NameParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Code")
