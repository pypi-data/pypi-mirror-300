from collections.abc import Iterator

from lxml.etree import QName, _Element  # type: ignore

from .base_parser import Sdmxv21Parser
from .errors import CategorySchemeNotFound
from .name_parser import NameParser

__all__ = ["CategoryParser", "CategorySchemeParser", "CategorySchemesParser"]


class BaseCategoryParser(NameParser):
    def iter_category_parsers(self) -> Iterator["CategoryParser"]:
        for category_element in self._iter_category_elements():
            yield CategoryParser(category_element, file=self.file)

    def _iter_category_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./str:Category")


class CategoryParser(BaseCategoryParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "Category")


class CategorySchemeParser(BaseCategoryParser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "CategoryScheme")


class CategorySchemesParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["structure"], "CategorySchemes")

    def create_category_scheme_parser(self, category_scheme_id: str) -> CategorySchemeParser:
        category_scheme_element = self._get_category_scheme_element(category_scheme_id)
        return CategorySchemeParser(category_scheme_element, file=self.file)

    def _get_category_scheme_element(self, category_scheme_id: str) -> _Element:
        try:
            return self.find_one(f"./str:CategoryScheme[@id='{category_scheme_id}']")
        except ValueError as exc:
            raise CategorySchemeNotFound(category_scheme_id, element=self.element) from exc
