from pathlib import Path
from typing import TYPE_CHECKING, AnyStr, Self, TypeVar

from lxml.etree import _Element  # type: ignore

from dbnomics_fetcher_toolbox.sdmx_utils.parsers import SdmxParser

from .namespaces import SDMX_v2_1_NAMESPACES

if TYPE_CHECKING:
    from lxml._types import _DefEtreeParsers  # type: ignore


__all__ = ["Sdmxv21Parser"]


TSdmxv21Parser = TypeVar("TSdmxv21Parser", bound="Sdmxv21Parser")


class Sdmxv21Parser(SdmxParser):
    def __init__(
        self,
        element: _Element,
        *,
        file: Path | None = None,
    ) -> None:
        super().__init__(
            element,
            file=file,
            namespaces=SDMX_v2_1_NAMESPACES,
        )

    @classmethod
    def from_xml_file(  # type: ignore
        cls,
        file: Path,
        *,
        etree_parser: "_DefEtreeParsers[_Element] | None" = None,
    ) -> Self:
        root = cls._parse_xml_file(file, etree_parser=etree_parser)
        return cls(root, file=file)

    @classmethod
    def from_xml_string(  # type: ignore
        cls,
        value: AnyStr,
        *,
        etree_parser: "_DefEtreeParsers[_Element] | None" = None,
    ) -> Self:
        root = cls._parse_xml_string(value, parser=etree_parser)
        return cls(root)
