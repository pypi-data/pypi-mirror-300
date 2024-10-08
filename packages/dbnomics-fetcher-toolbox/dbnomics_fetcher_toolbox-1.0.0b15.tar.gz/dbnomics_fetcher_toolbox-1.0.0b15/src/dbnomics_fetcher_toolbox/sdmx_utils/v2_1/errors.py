from lxml.etree import _Element  # type: ignore

from dbnomics_fetcher_toolbox.sdmx_utils.errors import SdmxParseError

__all__ = [
    "CategorySchemeNotFound",
    "CodelistNotFound",
    "ConceptNotFound",
    "DataflowNotFound",
    "DataSetNotFound",
]


class CategorySchemeNotFound(SdmxParseError):
    def __init__(self, category_scheme_id: str, *, element: _Element) -> None:
        msg = f"CategoryScheme {category_scheme_id!r} not found"
        super().__init__(element=element, msg=msg)
        self.category_scheme_id = category_scheme_id


class CodelistNotFound(SdmxParseError):
    def __init__(self, codelist_id: str, *, element: _Element) -> None:
        msg = f"Codelist {codelist_id!r} not found"
        super().__init__(element=element, msg=msg)
        self.codelist_id = codelist_id


class ConceptNotFound(SdmxParseError):
    def __init__(self, concept_id: str, *, element: _Element) -> None:
        msg = f"Concept {concept_id!r} not found"
        super().__init__(element=element, msg=msg)
        self.concept_id = concept_id


class ConceptSchemeNotFound(SdmxParseError):
    def __init__(self, concept_scheme_id: str, *, element: _Element) -> None:
        msg = f"ConceptScheme {concept_scheme_id!r} not found"
        super().__init__(element=element, msg=msg)
        self.concept_scheme_id = concept_scheme_id


class DataflowNotFound(SdmxParseError):
    def __init__(self, dataflow_id: str, *, element: _Element) -> None:
        msg = f"Dataflow {dataflow_id!r} not found"
        super().__init__(element=element, msg=msg)
        self.dataflow_id = dataflow_id


class DataSetNotFound(SdmxParseError):
    def __init__(self, *, element: _Element) -> None:
        msg = "DataSet not found"
        super().__init__(element=element, msg=msg)
