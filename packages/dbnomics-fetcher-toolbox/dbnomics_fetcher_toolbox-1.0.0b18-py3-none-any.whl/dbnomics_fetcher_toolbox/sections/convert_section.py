from collections.abc import Iterator
from contextlib import contextmanager
from typing import TYPE_CHECKING

import daiquiri
from contexttimer import Timer
from dbnomics_data_model.storage import Storage

from dbnomics_fetcher_toolbox._internal.formatters import format_timer
from dbnomics_fetcher_toolbox.sections.section import Section
from dbnomics_fetcher_toolbox.sections.skip_reasons import SkipReason
from dbnomics_fetcher_toolbox.types import SectionId, SectionPath

if TYPE_CHECKING:
    from dbnomics_fetcher_toolbox.helpers.converter_helper import ConverterHelper


__all__ = ["ConvertSection"]


logger = daiquiri.getLogger(__name__)


class ConvertSection(Section):
    def __init__(
        self,
        *,
        converter_helper: "ConverterHelper",
        fail_fast: bool,
        id: SectionId | str,
        parent_path: SectionPath,
        resume_mode: bool,
    ) -> None:
        super().__init__(fail_fast=fail_fast, id=id, parent_path=parent_path, resume_mode=resume_mode)
        self._converter_helper = converter_helper

    @contextmanager
    def start(self) -> Iterator[Storage]:
        logger.debug("Starting convert section %r", self.path_str)

        with (
            self._storage.create_session(self.id) as session,
            Timer() as timer,
        ):
            try:
                yield session.storage
            except Exception:
                if self._fail_fast:
                    raise
                logger.exception(
                    "Error during convert section %r",
                    self.path_str,
                    duration=format_timer(timer),
                )
                return

            session.commit()

        logger.debug(
            "Finished convert section %r",
            self.path_str,
            duration=format_timer(timer),
        )

    def _get_skip_reason(self) -> SkipReason | None:
        return self._get_skip_reason_for_options(fetcher_helper=self._converter_helper)

    @property
    def _storage(self) -> Storage:
        return self._converter_helper._storage  # type: ignore # noqa: SLF001
