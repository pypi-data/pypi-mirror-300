from pathlib import Path

from lxml.etree import QName, _Element  # type: ignore

from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError

__all__ = ["TextNotFound", "UnexpectedTag", "XmlElementParseError"]


class XmlElementParseError(FetcherToolboxError):
    def __init__(self, *, element: _Element, msg: str) -> None:
        super().__init__(msg=msg)
        self.element = element


class TextNotFound(XmlElementParseError):
    def __init__(self, *, element: _Element) -> None:
        msg = f"No text found in {element!r}"
        super().__init__(element=element, msg=msg)


class UnexpectedTag(XmlElementParseError):
    def __init__(self, *, element: _Element, expected_tag: QName, file: Path | None) -> None:
        msg = f"Expected tag {expected_tag} but received {element!r}, file={str(file)!r}"
        super().__init__(element=element, msg=msg)
        self.expected_tag = expected_tag
        self.file = file
