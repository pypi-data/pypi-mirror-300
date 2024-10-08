from typing import Final

from dbnomics_fetcher_toolbox.xml_utils.types import NamespaceDict

__all__ = ["SDMX_v2_1_NAMESPACES"]


SDMX_v2_1_NAMESPACES: Final[NamespaceDict] = {
    "com": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
    "common": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
    "data": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific",
    "footer": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message/footer",
    "gen": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
    "md": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/metadata/generic",
    "mes": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
    "message": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
    "str": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "structure": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}
