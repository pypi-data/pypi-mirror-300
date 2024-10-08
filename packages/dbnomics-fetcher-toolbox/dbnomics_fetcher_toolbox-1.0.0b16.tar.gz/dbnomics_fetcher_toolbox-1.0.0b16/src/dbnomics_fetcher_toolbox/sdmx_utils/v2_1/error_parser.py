from collections.abc import Iterator

from lxml.etree import QName, _Element  # type: ignore

from .base_parser import Sdmxv21Parser


class ErrorParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["message"], "Error")

    @property
    def error_message_parser(self) -> "ErrorMessageParser":
        error_message_element = self._error_message_element
        return ErrorMessageParser(error_message_element, file=self.file)

    @property
    def _error_message_element(self) -> _Element:
        return self.find_one("mes:ErrorMessage")


class ErrorMessageParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["message"], "ErrorMessage")

    @property
    def code(self) -> str:
        return self.element.attrib["code"]

    def iter_text_lines(self) -> Iterator[str]:
        for text_element in self._iter_text_elements():
            yield self.get_text(text_element)

    def _iter_text_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./com:Text")
