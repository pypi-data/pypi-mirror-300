import statistics
from collections import OrderedDict
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self

from dbnomics_data_model.json_utils import JsonObject
from dbnomics_data_model.model import Dimension, DimensionCode, DimensionValueCode

from dbnomics_fetcher_toolbox.partition_downloader.errors import PartitionDownloaderError, UnsplittablePartition
from dbnomics_fetcher_toolbox.partition_downloader.partitions.types import Partition

__all__ = ["DimensionPartition"]


@dataclass(kw_only=True)
class DimensionSelection:
    all_values: list[DimensionValueCode]
    selected_values: list[DimensionValueCode]

    @classmethod
    def create(cls, *, dimension: Dimension) -> Self:
        """Select all dimension values."""
        value_codes = [value.code for value in dimension.values]
        return cls(all_values=value_codes, selected_values=value_codes)

    def bisect(self) -> tuple[Self, Self]:
        index = len(self.selected_values) // 2
        left = self.__class__(all_values=self.all_values, selected_values=self.selected_values[:index])
        right = self.__class__(all_values=self.all_values, selected_values=self.selected_values[index:])
        return left, right

    @property
    def is_fully_selected(self) -> bool:
        return len(set(self.all_values)) == len(set(self.selected_values))

    def __iter__(self) -> Iterator[DimensionValueCode]:
        return iter(self.selected_values)

    def __len__(self) -> int:
        return len(self.selected_values)

    def __str__(self) -> str:
        return "" if self.is_fully_selected else "+".join(self.selected_values)


@dataclass(kw_only=True)
class DimensionFilter:
    selected_values: OrderedDict[DimensionCode, DimensionSelection]

    @classmethod
    def create(cls, *, dimensions: list[Dimension]) -> Self:
        """Select all values of each dimension."""
        selected_values = OrderedDict(
            (dimension.code, DimensionSelection.create(dimension=dimension)) for dimension in dimensions
        )
        return cls(selected_values=selected_values)

    @property
    def are_all_dimensions_fully_selected(self) -> bool:
        return all(selection.is_fully_selected for selection in self.selected_values.values())

    def bisect(self) -> tuple[Self, Self]:
        dimension_code_to_bisect = self._select_dimension_to_bisect()
        if dimension_code_to_bisect is None:
            raise UnsplittableDimensionFilter(self)

        left_selection, right_selection = self.selected_values[dimension_code_to_bisect].bisect()
        left = self.__class__(selected_values=self.selected_values | {dimension_code_to_bisect: left_selection})
        right = self.__class__(selected_values=self.selected_values | {dimension_code_to_bisect: right_selection})
        return left, right

    def __str__(self) -> str:
        return ".".join(str(selection) for selection in self.selected_values.values())

    def _select_dimension_to_bisect(self) -> DimensionCode | None:
        """Select the dimension having the "median low" number of values.

        To avoid both:

        * the one with the least values because it has a higher probability to return too many results
        * the one with the most values because it could lead to URL too long
        """
        candidates = [
            (selection_len, dimension_code)
            for dimension_code, selection in self.selected_values.items()
            if (selection_len := len(selection)) > 1
        ]
        if not candidates:
            return None
        return statistics.median_low(candidates)[1]


class DimensionPartition(Partition):
    def __init__(self, *, dimension_filter: DimensionFilter) -> None:
        self._dimension_filter = dimension_filter
        partition_id = str(self._dimension_filter)
        super().__init__(partition_id=partition_id)

    @classmethod
    def create(cls, *, dimensions: list[Dimension]) -> Self:
        dimension_filter = DimensionFilter.create(dimensions=dimensions)
        return cls(dimension_filter=dimension_filter)

    def bisect(self) -> tuple[Self, Self]:
        left_filter, right_filter = self._dimension_filter.bisect()
        left = self.__class__(dimension_filter=left_filter)
        right = self.__class__(dimension_filter=right_filter)
        return left, right

    @property
    def file_discriminator(self) -> str:
        return str(self._dimension_filter)

    def split(self) -> list[Self]:
        try:
            return list(self.bisect())
        except UnsplittableDimensionFilter as exc:
            raise UnsplittablePartition(partition=self) from exc

    def to_json(self) -> JsonObject:
        return {"filter": str(self._dimension_filter)}


class UnsplittableDimensionFilter(PartitionDownloaderError):
    def __init__(self, dimension_filter: DimensionFilter) -> None:
        msg = f"Dimension filter {dimension_filter} can't be split anymore"
        super().__init__(msg=msg)
        self.dimension_filter = dimension_filter
