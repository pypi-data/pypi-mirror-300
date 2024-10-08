from dbnomics_fetcher_toolbox.xml_utils.parsers import XmlParser

__all__ = ["SdmxParser"]


class SdmxParser(XmlParser):
    @property
    def id(self) -> str:
        return self.element.attrib["id"]
