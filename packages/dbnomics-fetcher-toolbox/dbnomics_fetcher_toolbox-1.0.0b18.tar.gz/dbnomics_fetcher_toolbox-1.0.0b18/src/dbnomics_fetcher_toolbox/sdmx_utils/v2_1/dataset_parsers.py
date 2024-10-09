from collections.abc import Iterator

from lxml.etree import QName, _Element  # type: ignore

from .base_parser import Sdmxv21Parser

__all__ = ["DataSetParser"]


class DataSetParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName(self._namespaces["message"], "DataSet")

    def iter_series_parsers(self) -> Iterator["SeriesParser"]:
        for series_element in self._iter_series_elements():
            yield SeriesParser(series_element, file=self.file)

    def _iter_series_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./Series")


class SeriesParser(Sdmxv21Parser):
    @property
    def __expected_tag__(self) -> QName | None:
        return QName("Series")

    def iter_obs_elements(self) -> Iterator[_Element]:
        yield from self.iterfind("./Obs")
