import contextlib
from pathlib import Path
from typing import Final

import pytest

from dbnomics_fetcher_toolbox.convert_cli import Converter
from dbnomics_fetcher_toolbox.converter_helper import DEFAULT_CONVERT_REPORT_FILENAME
from dbnomics_fetcher_toolbox.errors import DuplicateDataset

SOURCE_DATA_DIR_NAME: Final = "source-data"


def test_Converter__init__empty_args(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    class TestConverter(Converter):
        def __init__(self) -> None:
            super().__init__(args=[], base_dir=tmp_path)

        def process(self) -> None:
            pass

    with contextlib.suppress(SystemExit):
        TestConverter()

    output = capsys.readouterr().err
    assert "error: the following arguments are required: source_dir" in output


def test_Converter__init__not_call(tmp_path: Path) -> None:
    class TestConverter(Converter):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)
            self.run_was_successful = False

        def process(self) -> None:
            self.run_was_successful = True

    converter = TestConverter()

    assert not (converter._base_dir / DEFAULT_CONVERT_REPORT_FILENAME).is_file()
    assert not converter.run_was_successful


def test_Converter__init__call(tmp_path: Path) -> None:
    class TestConverter(Converter):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)
            self.run_was_successful = False

        def process(self) -> None:
            self.run_was_successful = True

    converter = TestConverter()
    converter()

    assert (converter._base_dir / DEFAULT_CONVERT_REPORT_FILENAME).is_file()
    assert converter.run_was_successful


def test_Converter__process_dataset__and__load_resource(foo_txt: Resource[bytes, bytes], tmp_path: Path) -> None:
    d1: Final = "D1"

    class TestConverter(Converter):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)
            self.process_d1_was_successful = False

        def process_d1(self, dataset_code: str) -> None:
            assert dataset_code == d1
            response = self.load_resource(foo_txt)
            assert isinstance(response, FilePathResponse)
            assert response.payload == self._source_dir / "foo.txt"
            self.process_d1_was_successful = True

        def process(self) -> None:
            converter.process_dataset(d1, self.process_d1)

    converter = TestConverter()
    converter()

    assert converter.process_d1_was_successful
    assert len(converter._state.successful) == 1
    assert converter._state.successful[0].resource_id == d1
    assert not converter._state.errors
    assert not converter._state.skips
    assert not converter._state.skipped_ids


def test_Converter__duplicate_dataset_code_fails(tmp_path: Path) -> None:
    class TestConverter(Converter):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)

        def process_d1(self, _: str) -> None:
            pass

        def process(self) -> None:
            converter.process_dataset("D1", self.process_d1)
            with pytest.raises(DuplicateDataset) as exc_info:
                converter.process_dataset("D1", self.process_d1)
            assert exc_info.value.dataset_code == "D1"

    converter = TestConverter()
    converter()
