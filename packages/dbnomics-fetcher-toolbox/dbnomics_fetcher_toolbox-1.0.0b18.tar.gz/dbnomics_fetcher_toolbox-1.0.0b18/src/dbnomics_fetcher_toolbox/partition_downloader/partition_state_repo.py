from collections import OrderedDict
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, Self, TypeVar, cast

from dbnomics_data_model.json_utils import JsonObject, load_json_file, save_json_file

from dbnomics_fetcher_toolbox._internal.import_utils import load_class_from_string
from dbnomics_fetcher_toolbox.partition_downloader.errors import StateFileLoadError, StateFileSaveError
from dbnomics_fetcher_toolbox.partition_downloader.partitions.types import Partition, PartitionId

__all__ = ["PartitionStateRepo"]


TPartition = TypeVar("TPartition", bound=Partition)


@dataclass
class PartitionsJson:
    partition_class: str
    splits: list[tuple[str, list[JsonObject]]]


class PartitionStateRepo(Generic[TPartition]):
    def __init__(self, *, file: Path, initial_splits: OrderedDict[PartitionId, list[TPartition]] | None = None) -> None:
        if initial_splits is None:
            initial_splits = OrderedDict()

        self._file = file

        self._splits: OrderedDict[PartitionId, list[TPartition]] = initial_splits

    @classmethod
    def from_file(cls, input_file: Path) -> Self:
        if not input_file.is_file():
            return cls(file=input_file)

        try:
            partitions_json = load_json_file(input_file, type_=PartitionsJson)
        except Exception as exc:
            raise StateFileLoadError(input_file) from exc

        class_path = partitions_json.partition_class
        partition_class = load_class_from_string(class_path)
        if not issubclass(partition_class, Partition):
            msg = f"Partition class {class_path} is not a subclass of {Partition.__name__}"
            raise TypeError(msg)

        initial_splits = cast(
            OrderedDict[PartitionId, list[TPartition]],
            OrderedDict(
                (
                    partition_id,
                    [partition_class.from_json(sub_partition_json) for sub_partition_json in sub_partitions_json],
                )
                for partition_id, sub_partitions_json in partitions_json.splits
            ),
        )
        return cls(file=input_file, initial_splits=initial_splits)

    def find_sub_partitions(self, partition_id: PartitionId) -> list[TPartition] | None:
        return self._splits.get(partition_id)

    def register_partition_split(self, partition_id: PartitionId, *, sub_partitions: Iterable[TPartition]) -> None:
        state_file = self._file
        self._splits[partition_id] = list(sub_partitions)
        json_data = self.to_json()
        state_file.parent.mkdir(exist_ok=True, parents=True)
        try:
            save_json_file(state_file, json_data)
        except Exception as exc:
            raise StateFileSaveError(state_file) from exc

    def to_json(self) -> PartitionsJson | None:
        if not self._splits:
            return None

        first_split_partitions = next(iter(self._splits.values()))
        if not first_split_partitions:
            return None

        partition = first_split_partitions[0]
        partition_class_name = f"{partition.__class__.__module__}.{partition.__class__.__name__}"

        splits = [
            (partition_id, [sub_partition.to_json() for sub_partition in sub_partitions])
            for partition_id, sub_partitions in self._splits.items()
        ]

        return PartitionsJson(partition_class=partition_class_name, splits=splits)
