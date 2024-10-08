from pathlib import Path

from dbnomics_data_model.model import DatasetId
from dbnomics_data_model.storage import StorageSession

from dbnomics_fetcher_toolbox.errors.base import FetcherToolboxError
from dbnomics_fetcher_toolbox.formatters import format_file_path
from dbnomics_fetcher_toolbox.sections.section import Section


class SectionError(FetcherToolboxError):
    def __init__(self, section: Section, *, msg: str) -> None:
        super().__init__(msg=msg)
        self.section = section


class DatasetSectionError(SectionError):
    pass


class DatasetNotSaved(DatasetSectionError):
    def __init__(self, dataset_id: DatasetId, *, section: Section, session: StorageSession) -> None:
        msg = (
            f"Dataset {dataset_id.dataset_code!r} was not found in storage after finishing section {section.path_str!r}"
        )
        super().__init__(section, msg=msg)
        self.dataset_id = dataset_id
        self.session = session


class FileSectionError(SectionError):
    pass


class FileNotWritten(FileSectionError):
    def __init__(self, file: Path, *, section: Section) -> None:
        msg = f"File {format_file_path(file)!r} was not found after finishing section {section.path_str!r}"
        super().__init__(section, msg=msg)
        self.file = file
