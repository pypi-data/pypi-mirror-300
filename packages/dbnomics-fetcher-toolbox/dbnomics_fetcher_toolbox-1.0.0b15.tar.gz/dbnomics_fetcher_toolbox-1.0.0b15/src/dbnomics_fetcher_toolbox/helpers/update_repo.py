from datetime import datetime
from pathlib import Path
from typing import Final, TypeAlias

import daiquiri
from dbnomics_data_model.json_utils import create_default_dumper, dump_as_json_data, load_json_file, save_json_file
from dbnomics_data_model.typedload_utils import create_default_loader
from typedload.datadumper import Dumper
from typedload.dataloader import Loader

from dbnomics_fetcher_toolbox.formatters import format_file_path, format_file_path_with_size
from dbnomics_fetcher_toolbox.helpers.constants import INCREMENTAL_MODE_PREFIX
from dbnomics_fetcher_toolbox.types import SectionId

__all__ = ["UpdateRepo"]


UpdatesDict: TypeAlias = dict[SectionId, datetime]

UPDATES_FILE_NAME: Final = "updates.json"

logger = daiquiri.getLogger(__name__)


class UpdateRepo:
    def __init__(self, *, all_updated_at: datetime | None = None, base_dir: Path) -> None:
        self._all_updated_at = all_updated_at
        self._base_dir = base_dir

        self._updates: UpdatesDict = {}

        self._dumper = self._create_dumper()
        self._loader = self._create_loader()

    def get_updated_at(self, section_id: SectionId) -> datetime | None:
        if self._all_updated_at is not None:
            return self._all_updated_at

        return self._updates.get(section_id)

    def load(self) -> None:
        if self._all_updated_at is not None:
            logger.debug(
                "%s is enabled, considering all resources to be updated at %s",
                INCREMENTAL_MODE_PREFIX,
                self._all_updated_at.isoformat(),
            )
            return

        updates_file = self._updates_file
        if updates_file.is_file():
            self._updates = load_json_file(updates_file, loader=self._loader, type_=UpdatesDict)
            logger.debug(
                "%s is enabled, loaded update dates from %s: %r",
                INCREMENTAL_MODE_PREFIX,
                format_file_path(updates_file),
                sorted(((v.isoformat(), k) for k, v in self._updates.items()), reverse=True),
            )
        else:
            logger.debug(
                "%s is disabled because updates file %r does not exist",
                INCREMENTAL_MODE_PREFIX,
                str(updates_file),
            )

    def save(self) -> None:
        if self._all_updated_at is not None:
            return

        updates_file = self._updates_file
        updates_data = dump_as_json_data(self._updates, dumper=self._dumper)
        save_json_file(updates_file, updates_data)
        logger.info("Updates file saved to %s", format_file_path_with_size(updates_file))

    def set_updated_at(self, section_id: SectionId, updated_at: datetime) -> None:
        if self._all_updated_at is not None:
            return

        self._updates[section_id] = updated_at

    def _create_dumper(self) -> Dumper:
        dumper = create_default_dumper()
        dumper.strconstructed.add(SectionId)  # type: ignore[reportUnknownMemberType]
        return dumper

    def _create_loader(self) -> Loader:
        loader = create_default_loader()
        loader.strconstructed.add(SectionId)  # type: ignore[reportUnknownMemberType]
        return loader

    @property
    def _updates_file(self) -> Path:
        return self._base_dir / UPDATES_FILE_NAME
