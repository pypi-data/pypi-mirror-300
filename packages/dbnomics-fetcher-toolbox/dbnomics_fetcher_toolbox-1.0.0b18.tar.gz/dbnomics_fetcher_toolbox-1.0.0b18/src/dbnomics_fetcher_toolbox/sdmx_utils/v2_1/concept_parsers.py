from collections.abc import Iterator

from lxml.etree import QName, _Element  # type: ignore

from .base_parser import Sdmxv21Parser
from .errors import ConceptNotFound, ConceptSchemeNotFound
from .name_parser import NameParser

__all__ = ["ConceptParser", "ConceptSchemeParser", "ConceptsParser"]


class ConceptsParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Concepts")

    def create_concept_scheme_parser(self, category_scheme_id: str) -> "ConceptSchemeParser":
        concept_scheme_element = self._get_concept_scheme_element(category_scheme_id)
        return ConceptSchemeParser(concept_scheme_element, file=self.file)

    def _get_concept_scheme_element(self, concept_scheme_id: str) -> _Element:
        try:
            return self.find_one(f"./str:ConceptScheme[@id='{concept_scheme_id}']")
        except ValueError as exc:
            raise ConceptSchemeNotFound(concept_scheme_id, element=self.element) from exc


class ConceptSchemeParser(Sdmxv21Parser):
    def __post_init__(self) -> None:
        self._concept_element_by_id: dict[str, _Element] = {}

    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "ConceptScheme")

    def create_concept_parser(self, concept_id: str) -> "ConceptParser":
        concept_element = self._get_concept_element(concept_id)
        return ConceptParser(concept_element, file=self.file)

    def iter_concept_parsers(self) -> Iterator["ConceptParser"]:
        for concept_element in self._iter_concept_elements():
            concept_parser = ConceptParser(concept_element, file=self.file)
            self._concept_element_by_id[concept_parser.id] = concept_element
            yield concept_parser

    def _get_concept_element(self, concept_id: str) -> _Element:
        concept_element = self._concept_element_by_id.get(concept_id)
        if concept_element is not None:
            return concept_element

        try:
            concept_element = self.find_one(f'./str:Concept[@id="{concept_id}"]')
        except ValueError as exc:
            raise ConceptNotFound(concept_id, element=self.element) from exc

        self._concept_element_by_id[concept_id] = concept_element
        return concept_element

    def _iter_concept_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./str:Concept")


class ConceptParser(NameParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Concept")
