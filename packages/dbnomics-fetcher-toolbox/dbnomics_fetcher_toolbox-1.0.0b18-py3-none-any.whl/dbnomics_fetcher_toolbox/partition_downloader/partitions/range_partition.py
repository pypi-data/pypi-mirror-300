from dataclasses import KW_ONLY, dataclass
from typing import Generic, Protocol, Self, TypeVar, cast

from dbnomics_data_model.json_utils import JsonObject, dump_as_json_data, load_json_data
from dbnomics_data_model.model import Period

from dbnomics_fetcher_toolbox.partition_downloader.errors import PartitionDownloaderError, UnsplittablePartition
from dbnomics_fetcher_toolbox.partition_downloader.partitions.types import Partition

__all__ = ["RangePartition", "PeriodRangePartition"]


class RangeValue(Protocol):
    def __add__(self, increment: int) -> Self: ...

    def __sub__(self, other: Self) -> int: ...

    @classmethod
    def parse(cls, value: str) -> Self: ...


TRangeValue = TypeVar("TRangeValue", bound=RangeValue)


class RangePartition(Partition, Generic[TRangeValue]):
    def __init__(
        self,
        min_value: TRangeValue,
        max_value: TRangeValue,
        *,
        max_length: int | None = None,
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.max_length = max_length
        partition_id = f"{self.min_value}__{self.max_value}"
        super().__init__(partition_id=partition_id)

    def __len__(self) -> int:
        return self.max_value - self.min_value

    def bisect(self) -> tuple[Self, Self]:
        if self.max_value == self.min_value:
            raise UnsplittableRange(self.min_value, self.max_value)

        middle_index = len(self) // 2
        middle_value = self.min_value + middle_index
        left = self.__class__(self.min_value, middle_value, max_length=self.max_length)
        right = self.__class__(middle_value + 1, self.max_value, max_length=self.max_length)
        return left, right

    @property
    def file_discriminator(self) -> str:
        return f"{self.min_value}-{self.max_value}"

    @property
    def should_pre_split(self) -> bool:
        return self.max_length is not None and len(self) >= self.max_length

    def split(self) -> list[Self]:
        try:
            return list(self.bisect())
        except UnsplittableRange as exc:
            raise UnsplittablePartition(partition=self) from exc

    def to_json(self) -> JsonObject:
        return cast(
            JsonObject,
            dump_as_json_data(
                RangePartitionJson(
                    str(self.min_value),
                    str(self.max_value),
                    max_length=self.max_length,
                )
            ),
        )


class PeriodRangePartition(RangePartition[Period]):
    @classmethod
    def from_json(cls, data: JsonObject) -> Self:
        json_model = load_json_data(data, type_=RangePartitionJson)
        min_period = Period.parse(json_model.min)
        max_period = Period.parse(json_model.max)
        return cls(min_period, max_period, max_length=json_model.max_length)


@dataclass
class RangePartitionJson:
    min: str
    max: str

    _: KW_ONLY
    max_length: int | None


class UnsplittableRange(PartitionDownloaderError):
    def __init__(self, min_value: TRangeValue, max_value: TRangeValue) -> None:
        msg = f"Range [{min_value!r}-{max_value!r}] can't be split anymore"
        super().__init__(msg=msg)
        self.min_value = min_value
        self.max_value = max_value
