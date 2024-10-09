from pathlib import Path
from typing import TYPE_CHECKING

from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.partition_downloader.partitions.types import Partition


class PartitionDownloaderError(FetcherToolboxError):
    pass


class StateFileError(PartitionDownloaderError):
    def __init__(self, *, msg: str, state_file: Path) -> None:
        super().__init__(msg=msg)
        self.state_file = state_file


class StateFileLoadError(StateFileError):
    def __init__(self, state_file: Path) -> None:
        msg = f"Could not load state file: {state_file}"
        super().__init__(msg=msg, state_file=state_file)


class StateFileSaveError(StateFileError):
    def __init__(self, state_file: Path) -> None:
        msg = f"Could not save state file: {state_file}"
        super().__init__(msg=msg, state_file=state_file)


class UnsplittablePartition(PartitionDownloaderError):
    def __init__(self, partition: "Partition") -> None:
        msg = f"Partition {partition.id!r} can't be split anymore"
        super().__init__(msg=msg)
        self.partition = partition
