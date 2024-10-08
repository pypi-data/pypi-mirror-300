from lxml.etree import QName  # type: ignore

from .base_parser import Sdmxv21Parser

__all__ = ["RefParser"]


class RefParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName("Ref")

    @property
    def class_(self) -> str | None:
        return self.element.attrib["class"]

    @property
    def maintainable_parent_id(self) -> str | None:
        return self.element.attrib.get("maintainableParentID")
