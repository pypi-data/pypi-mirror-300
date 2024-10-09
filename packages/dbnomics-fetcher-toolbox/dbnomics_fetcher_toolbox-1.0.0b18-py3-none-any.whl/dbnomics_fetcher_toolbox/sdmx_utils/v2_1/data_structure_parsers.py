from collections.abc import Iterator

import daiquiri
from lxml.etree import QName, _Element  # type: ignore

from .base_parser import Sdmxv21Parser
from .name_parser import NameParser
from .ref_parser import RefParser

__all__ = ["DataStructuresParser", "DataStructureParser"]


logger = daiquiri.getLogger(__name__)


class DataStructuresParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "DataStructures")

    def create_data_structure_parser(self, data_structure_id: str) -> "DataStructureParser":
        data_structure_element = self._get_data_structure_element(data_structure_id)
        return DataStructureParser(data_structure_element, file=self.file)

    def iter_data_structure_parsers(self) -> Iterator["DataStructureParser"]:
        for data_structure_element in self._iter_data_structure_elements():
            yield DataStructureParser(data_structure_element, file=self.file)

    def _get_data_structure_element(self, data_structure_id: str) -> _Element:
        return self.find_one(f"./str:DataStructure[@id='{data_structure_id}']")

    def _iter_data_structure_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./str:DataStructure")


class DataStructureParser(NameParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "DataStructure")

    def create_attribute_list_parser(self, attribute_list_id: str | None = None) -> "AttributeListParser":
        attribute_list_element = self._get_attribute_list_element(attribute_list_id)
        return AttributeListParser(attribute_list_element, file=self.file)

    def create_dimension_list_parser(self, dimension_list_id: str | None = None) -> "DimensionListParser":
        dimension_list_element = self._get_dimension_list_element(dimension_list_id)
        return DimensionListParser(dimension_list_element, file=self.file)

    def _get_attribute_list_element(self, attribute_list_id: str | None = None) -> _Element:
        if attribute_list_id is None:
            attribute_list_id = "AttributeDescriptor"

        return self.find_one(f'./str:DataStructureComponents/str:AttributeList[@id="{attribute_list_id}"]')

    def _get_dimension_list_element(self, dimension_list_id: str | None = None) -> _Element:
        if dimension_list_id is None:
            dimension_list_id = "DimensionDescriptor"

        return self.find_one(f'./str:DataStructureComponents/str:DimensionList[@id="{dimension_list_id}"]')


class ComponentParser(Sdmxv21Parser):
    @property
    def codelist_ref_parser(self) -> RefParser | None:
        codelist_ref_element = self._codelist_ref_element
        if codelist_ref_element is None:
            return None

        return RefParser(codelist_ref_element, file=self.file)

    @property
    def concept_ref_parser(self) -> RefParser:
        concept_ref_element = self._concept_ref_element
        return RefParser(concept_ref_element, file=self.file)

    @property
    def _codelist_ref_element(self) -> _Element | None:
        return self.find('./str:LocalRepresentation/str:Enumeration/Ref[@class="Codelist"]')

    @property
    def _concept_ref_element(self) -> _Element:
        return self.find_one('./str:ConceptIdentity/Ref[@class="Concept"]')


class AttributeListParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "AttributeList")

    def create_attribute_parser(self, attribute_id: str) -> "AttributeParser":
        attribute_element = self._get_attribute_element(attribute_id)
        return AttributeParser(attribute_element, file=self.file)

    def iter_attribute_parsers(self) -> Iterator["AttributeParser"]:
        for attribute_element in self._iter_attribute_elements():
            yield AttributeParser(attribute_element, file=self.file)

    def _get_attribute_element(self, attribute_id: str) -> _Element:
        return self.find_one(f'./str:Attribute[@id="{attribute_id}"]')

    def _iter_attribute_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./str:Attribute")


class AttributeParser(ComponentParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Attribute")


class DimensionListParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "DimensionList")

    def create_dimension_parser(self, dimension_id: str) -> "DimensionParser":
        dimension_element = self._get_dimension_element(dimension_id)
        return DimensionParser(dimension_element, file=self.file)

    def iter_dimension_parsers(self) -> Iterator["DimensionParser"]:
        for dimension_element in self._iter_dimension_elements():
            yield DimensionParser(dimension_element, file=self.file)

    def _get_dimension_element(self, dimension_id: str) -> _Element:
        return self.find_one(f'./str:Dimension[@id="{dimension_id}"]')

    def _iter_dimension_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./str:Dimension")


class DimensionParser(ComponentParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Dimension")

    @property
    def position(self) -> int:
        return int(self.element.attrib["position"])
