from collections.abc import Collection, Iterator
from pathlib import Path
from typing import TYPE_CHECKING

from lxml import etree

if TYPE_CHECKING:
    from lxml._types import _TagSelector  # type: ignore
    from lxml.etree import _Element  # type: ignore
    from lxml.etree._iterparse import _NoNSEventNames  # type: ignore[reportPrivateUsage]


__all__ = ["fast_iter", "iter_xml_elements"]


def fast_iter(context: "etree.iterparse[tuple[_NoNSEventNames, _Element]]") -> Iterator[tuple[str, "_Element"]]:
    """Iterate the elements of context keeping memory usage low.

    See Also
    --------
    - http://stackoverflow.com/a/12161078
    - based on Liza Daly's fast_iter https://web.archive.org/web/20210309115224/http://www.ibm.com/developerworks/xml/library/x-hiperfparse/ # noqa

    """
    for event, element in context:
        yield event, element
        # It's safe to call clear() here because no descendants will be accessed
        element.clear()
        # Also eliminate now-empty references from the root node to element
        for ancestor in element.xpath("ancestor-or-self::*"):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    del context


def iter_xml_elements(
    xml_file: Path,
    *,
    huge_tree: bool = True,
    tag: "_TagSelector | Collection[_TagSelector]",
) -> Iterator["_Element"]:
    context = etree.iterparse(xml_file, events=["end"], huge_tree=huge_tree, tag=tag)
    for _, element in fast_iter(context):
        yield element
