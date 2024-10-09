from collections.abc import Iterator

from lxml.etree import QName

from .base_parser import Sdmxv21Parser

__all__ = ["NameParser"]


class NameParser(Sdmxv21Parser):
    @property
    def names(self) -> dict[str, str]:
        return dict(self._iter_names())

    def _iter_names(self) -> Iterator[tuple[str, str]]:
        for name_element in self.iterfind("./com:Name"):
            lang = name_element.attrib[QName(self._namespaces["xml"], "lang")]
            name = self.get_text(name_element)
            yield lang, name
