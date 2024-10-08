from lxml.etree import QName, _Element  # type: ignore

from .base_parser import Sdmxv21Parser
from .categorisation_parsers import CategorisationsParser
from .category_parsers import CategorySchemesParser
from .codelist_parsers import CodelistsParser
from .concept_parsers import ConceptsParser
from .data_structure_parsers import DataStructuresParser
from .dataflow_parsers import DataflowsParser
from .dataset_parsers import DataSetParser
from .errors import DataSetNotFound

__all__ = ["StructureParser", "StructureSpecificDataParser"]


class StructureParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["message"], "Structure")

    @property
    def categorisations_parser(self) -> CategorisationsParser:
        return CategorisationsParser(self._categorisations_element, file=self.file)

    @property
    def category_schemes_parser(self) -> CategorySchemesParser:
        return CategorySchemesParser(self._category_schemes_element, file=self.file)

    @property
    def codelists_parser(self) -> CodelistsParser:
        return CodelistsParser(self._codelists_element, file=self.file)

    @property
    def concepts_parser(self) -> ConceptsParser:
        return ConceptsParser(self._concepts_element, file=self.file)

    @property
    def data_structures_parser(self) -> DataStructuresParser:
        return DataStructuresParser(self._data_structures_element, file=self.file)

    @property
    def dataflows_parser(self) -> DataflowsParser:
        return DataflowsParser(self._dataflows_element, file=self.file)

    @property
    def _categorisations_element(self) -> _Element:
        return self.find_one("./mes:Structures/structure:Categorisations")

    @property
    def _category_schemes_element(self) -> _Element:
        return self.find_one("./mes:Structures/str:CategorySchemes")

    @property
    def _codelists_element(self) -> _Element:
        return self.find_one("./mes:Structures/str:Codelists")

    @property
    def _concepts_element(self) -> _Element:
        return self.find_one("./mes:Structures/str:Concepts")

    @property
    def _data_structures_element(self) -> _Element:
        return self.find_one("./mes:Structures/str:DataStructures")

    @property
    def _dataflows_element(self) -> _Element:
        return self.find_one("./mes:Structures/str:Dataflows")


class StructureSpecificDataParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["message"], "StructureSpecificData")

    @property
    def dataset_parser(self) -> DataSetParser:
        return DataSetParser(self._dataset_element, file=self.file)

    @property
    def _dataset_element(self) -> _Element:
        try:
            return self.find_one("./mes:DataSet")
        except ValueError as exc:
            raise DataSetNotFound(element=self.element) from exc
