import re
from pathlib import Path
from typing import TypeAlias, TypedDict

from dbnomics_data_model.storage import Storage
from phantom.re import FullMatch

__all__ = ["SectionId", "SectionPath"]


# Don't allow ":" because it is a forbidden character in Windows file names.
class SectionId(FullMatch, pattern=re.compile(r"[\w-]+")):
    __slots__ = ()


SectionPath: TypeAlias = list[SectionId]


class BaseKwargsFromCli(TypedDict):
    excluded: list[SectionId] | None
    fail_fast: bool
    report_file: Path | None
    resume_mode: bool
    selected: list[SectionId] | None


class ConverterHelperKwargsFromCli(BaseKwargsFromCli):
    source_dir: Path
    target_storage: Storage


class DownloaderHelperKwargsFromCli(BaseKwargsFromCli):
    cache_dir: Path | None
    debug_dir: Path | None
    is_incremental: bool
    state_dir: Path
    target_dir: Path
