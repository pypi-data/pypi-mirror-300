from pathlib import Path

from lxml import etree
from lxml.etree import _Element  # type: ignore

__all__ = ["write_xml_element"]


def write_xml_element(xml_file_path: Path, xml_element: _Element) -> None:
    with xml_file_path.open("wb") as xml_file:
        etree.ElementTree(xml_element).write(
            xml_file,
            encoding="utf-8",
            pretty_print=True,
            xml_declaration=True,
        )
