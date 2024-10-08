from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING, Generic, TypeVar, cast

import daiquiri
from contexttimer import Timer
from humanfriendly.text import pluralize

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox.formatters import format_file_path, format_file_path_with_size
from dbnomics_fetcher_toolbox.helpers.constants import RESUME_MODE_PREFIX
from dbnomics_fetcher_toolbox.helpers.downloader_helper import DownloaderHelper
from dbnomics_fetcher_toolbox.partition_downloader.partition_state_repo import PartitionStateRepo
from dbnomics_fetcher_toolbox.partition_downloader.partitions.types import Partition
from dbnomics_fetcher_toolbox.types import SectionId

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.sections.file_section import FileSection

__all__ = ["EnqueueSubPartitions", "PartitionDownloader"]


logger = daiquiri.getLogger(__name__)


TPartition = TypeVar("TPartition", bound=Partition)


class PartitionDownloader(ABC, Generic[TPartition]):
    def __init__(
        self,
        *,
        downloader_helper: DownloaderHelper,
        file_section: "FileSection",
        root_partition: TPartition,
    ) -> None:
        self._file_section = file_section

        self._fail_fast = downloader_helper._fail_fast  # noqa: SLF001 # type: ignore
        self._resume_mode = downloader_helper._resume_mode  # noqa: SLF001 # type: ignore
        self._state_dir = downloader_helper._state_dir  # noqa: SLF001 # type: ignore
        self._target_dir = downloader_helper.target_dir

        root_depth = 0
        self._partition_queue = deque([(root_partition, root_depth)])
        self._state = PartitionStateRepo[TPartition].from_file(self._state_file)

    def start(self) -> None:
        partition_files: list[Path] = []

        with Timer() as timer:
            partition_num = 0
            while self._partition_queue:
                partition, partition_depth = self._partition_queue.popleft()
                partition_num += 1
                partition_file = self._process_partition(
                    partition, partition_depth=partition_depth, partition_num=partition_num
                )
                if partition_file is not None:
                    partition_files.append(partition_file)

        logger.debug(
            "Downloaded %s in section %r",
            pluralize(len(partition_files), "partition"),
            self._file_section.id,
            duration=format_timer(timer),
            section=self._file_section.path_str,
        )

        if len(partition_files) == 1:
            first_partition_file = partition_files[0]
            first_partition_file.rename(self._file_section.file)
            logger.debug(
                "Moved the file of the only partition %s to %s",
                format_file_path(first_partition_file),
                format_file_path_with_size(self._file_section.file),
                section=self._file_section.path_str,
            )
        elif len(partition_files) > 1:
            logger.debug("Merging %s...", pluralize(len(partition_files), "partition"))
            self._merge_partitions(partition_files)
            for partition_file in partition_files:
                partition_file.unlink()
            logger.debug(
                "Merged (then deleted) %s to %s",
                pluralize(len(partition_files), "partition"),
                format_file_path_with_size(self._file_section.file),
                section=self._file_section.path_str,
            )

    @abstractmethod
    def _download_partition(self, partition: TPartition, *, section: "FileSection") -> None:
        raise NotImplementedError

    def _enqueue_partitions(self, partitions: Iterable[TPartition], *, partition_depth: int) -> None:
        for partition in partitions:
            self._partition_queue.append((partition, partition_depth + 1))

    def _get_partition_file(self, partition: TPartition) -> Path:
        section_file = self._file_section._target_file  # type: ignore # noqa: SLF001
        return section_file.with_stem(f"{section_file.stem}.partition-{partition.file_discriminator}")

    @abstractmethod
    def _merge_partitions(self, files: list[Path]) -> None:
        raise NotImplementedError

    def _process_partition(self, partition: TPartition, *, partition_depth: int, partition_num: int) -> Path | None:
        if self._resume_mode and (sub_partitions := self._state.find_sub_partitions(partition.id)) is not None:
            logger.debug(
                "%s Splitting the partition #%d %r instead of processing it, because it was previously split",
                RESUME_MODE_PREFIX,
                partition_num,
                partition.id,
                depth=partition_depth,
            )
            self._enqueue_partitions(sub_partitions, partition_depth=partition_depth)
            return None

        # Do this after resume mode, because resume mode is more predictible.
        if partition.should_pre_split:
            sub_partitions = partition.split()
            sub_partition_ids = [partition.id for partition in sub_partitions]
            logger.debug(
                "Partition #%d %r has been pre-split in %s instead of processing it: %r",
                partition_num,
                partition.id,
                pluralize(len(sub_partitions), "sub-partition"),
                sub_partition_ids,
                depth=partition_depth,
            )
            self._enqueue_partitions(sub_partitions, partition_depth=partition_depth)
            return None

        partition_file_section_id = SectionId.parse(f"partition{partition_num}")
        partition_file_section = self._file_section.create_file_subsection(
            self._get_partition_file(partition),
            id=partition_file_section_id,
            keep=False,
            # Don't use optional, so that a partition that fails makes the whole process fail.
            optional=False,
        )
        partition_file = partition_file_section.file
        if partition_file_section.is_skipped:
            return partition_file

        with partition_file_section.start():
            logger.debug(
                "Starting to download partition #%d %r to %s...",
                partition_num,
                partition.id,
                format_file_path(partition_file),
                depth=partition_depth,
                section=partition_file_section.path_str,
            )

            try:
                self._download_partition(partition, section=partition_file_section)
            except EnqueueSubPartitions as exc:
                sub_partitions = cast(list[TPartition], list(exc.sub_partitions))
                self._enqueue_partitions(sub_partitions, partition_depth=partition_depth)
                self._state.register_partition_split(partition.id, sub_partitions=sub_partitions)
                return None
            except Exception:
                if self._fail_fast:
                    raise
                logger.exception(
                    "Partition #%d %r could not be download, abort downloading all partitions",
                    partition_num,
                    partition.id,
                    depth=partition_depth,
                )
                raise

            logger.debug(
                "Partition #%d %r has been downloaded successfully to %s",
                partition_num,
                partition.id,
                format_file_path_with_size(partition_file),
                depth=partition_depth,
                section=partition_file_section.path_str,
            )

        return partition_file

    @property
    def _state_file(self) -> Path:
        return self._state_dir / f"partitions.{self._file_section.path_str}.json"


class EnqueueSubPartitions(Exception):
    def __init__(self, sub_partitions: Iterable[Partition]) -> None:
        super().__init__()
        self.sub_partitions = sub_partitions
