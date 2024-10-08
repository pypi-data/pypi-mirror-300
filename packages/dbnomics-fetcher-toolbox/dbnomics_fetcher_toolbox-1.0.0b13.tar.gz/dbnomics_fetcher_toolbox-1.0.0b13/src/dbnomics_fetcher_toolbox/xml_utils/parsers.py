from collections.abc import Iterator
from pathlib import Path
from typing import TYPE_CHECKING, AnyStr, Final, Self, cast

from lxml import etree
from lxml.etree import QName, _Element  # type: ignore
from more_itertools import one

from dbnomics_fetcher_toolbox.sentinels import UNINITIALIZED, Uninitialized
from dbnomics_fetcher_toolbox.xml_utils.errors import TextNotFound, UnexpectedTag
from dbnomics_fetcher_toolbox.xml_utils.types import NamespaceDict

if TYPE_CHECKING:
    from lxml._types import _DefEtreeParsers, _ElemPathArg  # type: ignore


__all__ = ["XmlParser"]


DEFAULT_XML_PARSER: Final = etree.XMLParser(huge_tree=True, remove_blank_text=True)


class XmlParser:
    def __init__(
        self,
        element: _Element,
        *,
        file: Path | None = None,
        namespaces: NamespaceDict | None = None,
    ) -> None:
        self.element = element
        self.file = file

        if namespaces is None:
            namespaces = cast(NamespaceDict, {})
        self._namespaces = namespaces

        expected_tag = self.__expected_tag__
        if expected_tag is not None and QName(element) != expected_tag:
            raise UnexpectedTag(element=element, expected_tag=expected_tag, file=self.file)

        self.__post_init__()

    def __post_init__(self) -> None:
        pass

    @classmethod
    def from_xml_file(
        cls,
        file: Path,
        *,
        namespaces: NamespaceDict | None = None,
        parser: "_DefEtreeParsers[_Element] | None" = None,
    ) -> Self:
        root = cls._parse_xml_file(file, etree_parser=parser)
        return cls(root, file=file, namespaces=namespaces)

    @classmethod
    def from_xml_string(
        cls,
        value: AnyStr,
        *,
        namespaces: NamespaceDict,
        parser: "_DefEtreeParsers[_Element] | None" = None,
    ) -> Self:
        root = cls._parse_xml_string(value, parser=parser)
        return cls(root, namespaces=namespaces)

    @property
    def __expected_tag__(self) -> QName | None:
        return None

    def dump(self) -> None:
        return etree.dump(self.element)

    def find(self, path: "_ElemPathArg", *, element: _Element | None = None) -> _Element | None:
        if element is None:
            element = self.element

        return element.find(path, namespaces=self._namespaces)

    def find_one(self, path: "_ElemPathArg", *, element: _Element | None = None) -> _Element:
        return one(self.iterfind(path, element=element))

    def get_text(self, element_or_path: "_Element | _ElemPathArg | None" = None, *, strip: bool = True) -> str:
        element = (
            self.element
            if element_or_path is None
            else element_or_path
            if isinstance(element_or_path, _Element)
            else self.find_one(element_or_path)
        )
        text = element.text
        if text is None:
            raise TextNotFound(element=element)

        if strip:
            text = text.strip()
        return text

    def iterfind(self, path: "_ElemPathArg", *, element: _Element | None = None) -> Iterator[_Element]:
        if element is None:
            element = self.element

        yield from element.iterfind(path, namespaces=self._namespaces)

    @classmethod
    def _parse_xml_file(
        cls, file: Path, *, etree_parser: "_DefEtreeParsers[_Element] | Uninitialized | None" = UNINITIALIZED
    ) -> _Element:
        return _parse_xml_file(file, parser=etree_parser)

    @classmethod
    def _parse_xml_string(
        cls, value: AnyStr, *, parser: "_DefEtreeParsers[_Element] | Uninitialized | None" = UNINITIALIZED
    ) -> _Element:
        return _parse_xml_string(value, parser=parser)


def _parse_xml_file(
    file: Path,
    *,
    parser: "_DefEtreeParsers[_Element] | Uninitialized | None" = UNINITIALIZED,
) -> _Element:
    if isinstance(parser, Uninitialized):
        parser = DEFAULT_XML_PARSER
    return etree.parse(str(file), parser=parser).getroot()


def _parse_xml_string(
    value: AnyStr,
    *,
    parser: "_DefEtreeParsers[_Element] | Uninitialized | None" = UNINITIALIZED,
) -> _Element:
    if isinstance(parser, Uninitialized):
        parser = DEFAULT_XML_PARSER
    return etree.fromstring(value, parser=parser)
