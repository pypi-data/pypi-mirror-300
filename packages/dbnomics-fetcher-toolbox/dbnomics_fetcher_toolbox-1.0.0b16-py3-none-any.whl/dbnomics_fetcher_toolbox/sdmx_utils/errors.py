from lxml.etree import _Element  # type: ignore

from dbnomics_fetcher_toolbox.xml_utils.errors import XmlElementParseError

__all__ = ["NameNotFound", "SdmxParseError"]


class SdmxParseError(XmlElementParseError):
    pass


class NameNotFound(XmlElementParseError):
    def __init__(self, *, element: _Element) -> None:
        msg = f"Name not found for element {element!r}"
        super().__init__(element=element, msg=msg)
