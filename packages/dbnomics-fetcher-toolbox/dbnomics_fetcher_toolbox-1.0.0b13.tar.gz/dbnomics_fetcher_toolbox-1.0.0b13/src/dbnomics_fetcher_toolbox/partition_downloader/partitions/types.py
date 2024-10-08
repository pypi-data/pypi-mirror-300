from abc import ABC, abstractmethod
from typing import Self, TypeAlias

from dbnomics_data_model.json_utils import JsonObject

__all__ = ["Partition", "PartitionId"]


PartitionId: TypeAlias = str


class Partition(ABC):
    def __init__(self, *, partition_id: PartitionId) -> None:
        self.id = partition_id

    @classmethod
    @abstractmethod
    def from_json(cls, data: JsonObject) -> Self:
        raise NotImplementedError

    @property
    @abstractmethod
    def file_discriminator(self) -> str:
        raise NotImplementedError

    @property
    def should_pre_split(self) -> bool:
        """Return True if the partition should not be downloaded, but split and ignored.

        Useful when the partition parameters clearly show that attempting downloading the partition would not work.
        """
        return False

    def split(self) -> list[Self]:
        raise NotImplementedError

    @abstractmethod
    def to_json(self) -> JsonObject:
        raise NotImplementedError
