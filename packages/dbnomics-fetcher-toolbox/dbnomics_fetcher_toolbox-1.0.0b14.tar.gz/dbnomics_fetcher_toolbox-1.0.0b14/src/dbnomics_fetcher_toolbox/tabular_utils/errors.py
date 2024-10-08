from typing import TYPE_CHECKING

from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from dbnomics_fetcher_toolbox.errors import FetcherToolboxError

if TYPE_CHECKING:
    from openpyxl.cell import _CellValue  # type:ignore[reportPrivateUsage]


__all__ = ["ExpectedEmptyCell", "UnexpectedCellValue", "WorksheetDataLoadError"]


class WorksheetDataLoadError(FetcherToolboxError):
    pass


class UnexpectedCellValue(WorksheetDataLoadError):
    def __init__(self, *, cell: Cell, expected_cell_value: "_CellValue", worksheet: Worksheet) -> None:
        msg = f"Got cell value {cell.value!r} at {cell.coordinate} in worksheet {worksheet.title}, expected {expected_cell_value!r}"  # noqa: E501
        super().__init__(msg=msg)
        self.cell = cell
        self.expected_cell_value = expected_cell_value
        self.worksheet = worksheet


class ExpectedEmptyCell(WorksheetDataLoadError):
    def __init__(self, *, cell: Cell, worksheet: Worksheet) -> None:
        msg = (
            f"Got cell value {cell.value!r} at {cell.coordinate} in worksheet {worksheet.title}, expected an empty cell"
        )
        super().__init__(msg=msg)
        self.cell = cell
        self.worksheet = worksheet
