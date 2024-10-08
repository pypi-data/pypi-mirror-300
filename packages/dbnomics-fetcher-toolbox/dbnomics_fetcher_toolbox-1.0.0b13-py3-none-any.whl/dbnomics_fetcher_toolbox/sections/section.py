from abc import ABC, abstractmethod

import daiquiri

from dbnomics_fetcher_toolbox.helpers.base_fetcher_helper import BaseFetcherHelper
from dbnomics_fetcher_toolbox.sections.skip_reasons import SkipReason
from dbnomics_fetcher_toolbox.types import SectionId, SectionPath

__all__ = ["Section"]

logger = daiquiri.getLogger(__name__)


class Section(ABC):
    def __init__(
        self,
        *,
        fail_fast: bool,
        id: SectionId | str,
        parent_path: SectionPath,
        resume_mode: bool,
    ) -> None:
        self.id = SectionId.parse(id)

        self._fail_fast = fail_fast
        self._parent_path = parent_path
        self._resume_mode = resume_mode

    @property
    def is_skipped(self) -> bool:
        skip_reason = self._get_skip_reason()
        if skip_reason is None:
            return False

        if skip_reason.log_message:
            logger.debug(skip_reason.message, section=self.path_str)

        self._post_is_skipped(skip_reason=skip_reason)
        return True

    @property
    def path(self) -> SectionPath:
        return [*self._parent_path, self.id]

    @property
    def path_str(self) -> str:
        return ".".join(self.path)

    @property
    def root_section_id(self) -> SectionId:
        return self.path[0]

    @abstractmethod
    def _get_skip_reason(self) -> SkipReason | None:
        raise NotImplementedError

    def _get_skip_reason_for_options(self, *, fetcher_helper: BaseFetcherHelper) -> SkipReason | None:
        root_section_id = self.root_section_id

        excluded = fetcher_helper._excluded  # type: ignore # noqa: SLF001
        matched_excluded = fetcher_helper._matched_excluded  # type: ignore # noqa: SLF001
        if excluded is not None and root_section_id in excluded:
            matched_excluded.add(root_section_id)
            return SkipReason(f"Skipping section {root_section_id!r} because it was excluded")

        selected = fetcher_helper._selected  # type: ignore # noqa: SLF001
        matched_selected = fetcher_helper._matched_selected  # type: ignore # noqa: SLF001
        if selected is not None:
            if root_section_id in selected:
                matched_selected.add(root_section_id)
            else:
                return SkipReason(
                    f"Skipping section {root_section_id!r} because it was not selected",
                    log_message=False,
                )

        return None

    def _post_is_skipped(self, *, skip_reason: SkipReason) -> None:  # noqa: ARG002
        return
