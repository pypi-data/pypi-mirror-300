import contextlib
from pathlib import Path
from typing import Final, cast

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from dbnomics_fetcher_toolbox.download_cli import Downloader
from dbnomics_fetcher_toolbox.downloader_helper import (
    DEFAULT_CACHE_DIR_NAME,
    DEFAULT_DEBUG_DIR_NAME,
    DEFAULT_DOWNLOAD_REPORT_FILENAME,
)
from dbnomics_fetcher_toolbox.errors import DuplicateSection, ResourceProcessingError
from tests.conftest import DummySource, MakeTxtResourceFixture

SOURCE_DATA_DIR_NAME: Final = "source-data"


def test_Downloader__init__empty_args(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[], base_dir=tmp_path)

        def process(self) -> None:
            pass

    with contextlib.suppress(SystemExit):
        TestDownloader()
    output = capsys.readouterr().err
    assert "error: the following arguments are required: target_dir" in output


def test_Downloader__init__no_call(tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)
            self.run_was_successful = False

        def process(self) -> None:
            self.run_was_successful = True

    downloader = TestDownloader()

    assert not (downloader._base_dir / DEFAULT_CACHE_DIR_NAME).is_dir()
    assert not (downloader._base_dir / DEFAULT_DEBUG_DIR_NAME).is_dir()
    assert not (downloader._base_dir / SOURCE_DATA_DIR_NAME).is_dir()
    assert not (downloader._base_dir / DEFAULT_DOWNLOAD_REPORT_FILENAME).is_file()
    assert not downloader.run_was_successful


def test_Downloader__init__call(tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)
            self.run_was_successful = False

        def process(self) -> None:
            self.run_was_successful = True

    downloader = TestDownloader()
    downloader()

    assert (downloader._base_dir / DEFAULT_CACHE_DIR_NAME).is_dir()
    assert (downloader._base_dir / DEFAULT_DEBUG_DIR_NAME).is_dir()
    assert (downloader._base_dir / SOURCE_DATA_DIR_NAME).is_dir()
    assert (downloader._base_dir / DEFAULT_DOWNLOAD_REPORT_FILENAME).is_file()
    assert downloader.run_was_successful


def test_Downloader__process_resource(foo_txt: Resource[bytes, bytes], tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)

        def process(self) -> None:
            response, error = self.download_resource(foo_txt)
            assert response is not None
            assert error is None

    downloader = TestDownloader()
    downloader()

    assert cast(DummySource, foo_txt.source).fetch_was_successful
    assert downloader._state.attempted_ids == ["foo"]
    assert len(downloader._state.successful) == 1
    assert downloader._state.successful[0].resource_id == "foo"
    assert not downloader._state.errors
    assert not downloader._state.skips
    assert not downloader._state.skipped_ids
    assert (downloader._target_dir / "foo.txt").is_file()


def test_Downloader__process_resource__error(foo_txt_with_error: Resource[bytes, bytes], tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)

        def process(self) -> None:
            response, error = self.download_resource(foo_txt_with_error)
            assert response is None
            assert error is not None

    downloader = TestDownloader()
    downloader()

    assert not cast(DummySource, foo_txt_with_error.source).fetch_was_successful
    assert downloader._state.attempted_ids == ["foo"]
    assert len(downloader._state.successful) == 0
    assert len(downloader._state.errors) == 1
    assert isinstance(downloader._state.errors[0], ResourceProcessingError)
    assert len(downloader._state.skips) == 0
    assert len(downloader._state.skipped_ids) == 0
    assert not (downloader._target_dir / "foo.txt").is_file()


def test_Downloader__process_resource__exclude(foo_txt: Resource[bytes, bytes], tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME, "--exclude=foo"], base_dir=tmp_path)

        def process(self) -> None:
            self.download_resource(foo_txt)

    downloader = TestDownloader()
    downloader()

    assert not cast(DummySource, foo_txt.source).fetch_was_successful
    assert len(downloader._state.attempted_ids) == 0
    assert len(downloader._state.successful) == 0
    assert len(downloader._state.errors) == 0
    assert len(downloader._state.skips) == 1
    assert downloader._state.skips[0] == ("foo", "Skipping resource 'foo' because it was excluded")
    assert len(downloader._state.skipped_ids) == 1
    assert downloader._state.skipped_ids[0] == "foo"
    assert not (downloader._target_dir / "foo.txt").is_file()


@pytest.mark.parametrize(
    ("option_name", "resource_ids", "expected_foo_called", "expected_bar_called"),
    [
        ("--exclude", "", True, True),
        ("--exclude", "foo", False, True),
        ("--exclude", "bar", True, False),
        ("--exclude", "foo,bar", False, False),
        ("--exclude", "foo, bar", False, False),
        ("--only", "", False, False),
        ("--only", "foo", True, False),
        ("--only", "bar", False, True),
        ("--only", "foo,bar", True, True),
        ("--only", "foo, bar", True, True),
    ],
)
def test_Downloader__exclude_or_only_cli_options(
    option_name: str,
    resource_ids: str,
    expected_foo_called: bool,
    expected_bar_called: bool,
    make_txt_resource: MakeTxtResourceFixture,
    tmp_path: Path,
) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME, f"{option_name}={resource_ids}"], base_dir=tmp_path)

        def process(self) -> None:
            self.download_resource(foo_txt)
            self.download_resource(bar_txt)

    foo_txt = make_txt_resource("foo")
    bar_txt = make_txt_resource("bar")

    downloader = TestDownloader()
    downloader()

    assert expected_foo_called == cast(DummySource, foo_txt.source).fetch_was_successful
    assert expected_bar_called == cast(DummySource, bar_txt.source).fetch_was_successful


def test_Downloader__exclude_and_only_cli_options_are_mutually_exclusive(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME, "--exclude=foo", "--only=bar"], base_dir=tmp_path)

        def process(self) -> None:
            pass

    with contextlib.suppress(SystemExit):
        TestDownloader()

    output = capsys.readouterr().err
    assert "error: argument --only: not allowed with argument --exclude" in output


@pytest.mark.parametrize("option_name", ["--exclude", "--only"])
@pytest.mark.parametrize("resource_ids", [" ", "a;b", "a;b, c"])
def test_Downloader__exclude_or_only_cli_options__invalid(
    option_name: str, resource_ids: str, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME, f"{option_name}={resource_ids}"], base_dir=tmp_path)

        def process(self) -> None:
            pass

    with contextlib.suppress(SystemExit):
        TestDownloader()

    output = capsys.readouterr().err
    assert f"error: argument {option_name}: invalid csv_resource_ids value: {resource_ids!r}" in output


def test_Downloader__fail_fast_cli_option(foo_txt_with_error: Resource[bytes, bytes], tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME, "--fail-fast"], base_dir=tmp_path)

        def process(self) -> None:
            self.download_resource(foo_txt_with_error)

    downloader = TestDownloader()
    with pytest.raises(ValueError, match="Dummy fetch error"):
        downloader()

    assert not cast(DummySource, foo_txt_with_error.source).fetch_was_successful
    assert downloader._state.attempted_ids == ["foo"]
    assert len(downloader._state.successful) == 0
    assert len(downloader._state.errors) == 1
    assert isinstance(downloader._state.errors[0], ResourceProcessingError)
    assert len(downloader._state.skips) == 0
    assert len(downloader._state.skipped_ids) == 0


def test_Downloader__limit(make_txt_resource: MakeTxtResourceFixture, tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME, "--limit=1"], base_dir=tmp_path)

        def process(self) -> None:
            self.download_resource(foo_txt)
            self.download_resource(bar_txt)

    foo_txt = make_txt_resource("foo")
    bar_txt = make_txt_resource("bar")

    downloader = TestDownloader()
    downloader()

    assert downloader._state.attempted_ids == ["foo"]
    assert downloader._state.skipped_ids == ["bar"]
    assert len(downloader._state.errors) == 0
    assert len(downloader._state.successful) == 1
    assert downloader._state.successful[0].resource_id == "foo"
    assert (downloader._target_dir / "foo.txt").is_file()
    assert not (downloader._target_dir / "bar.txt").is_file()


@given(limit=st.integers(max_value=0))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_Downloader__limit__failing(limit: int, capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME, f"--limit={limit}"], base_dir=tmp_path)

        def process(self) -> None:
            pass

    with contextlib.suppress(SystemExit):
        TestDownloader()

    output = capsys.readouterr().err
    assert f"error: argument --limit: Number '{limit}' must be positive" in output


def test_Downloader__duplicate_resource_id_fails(foo_txt: Resource[bytes, bytes], tmp_path: Path) -> None:
    class TestDownloader(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)

        def process(self) -> None:
            self.download_resource(foo_txt)

    downloader = TestDownloader()
    with pytest.raises(DuplicateSection) as exc_info:
        downloader()

    assert exc_info.value.section_id == "foo"


def test_Downloader__process_resource__existing_file(foo_txt: Resource[bytes, bytes], tmp_path: Path) -> None:
    class TestDownloader1(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)

        def process(self) -> None:
            response, error = self.download_resource(foo_txt)
            assert isinstance(response, BytesResponse)
            assert error is None
            assert (self._target_dir / "foo.txt").is_file()

    downloader1 = TestDownloader1()
    downloader1()

    class TestDownloader2(Downloader):
        def __init__(self) -> None:
            super().__init__(args=[SOURCE_DATA_DIR_NAME], base_dir=tmp_path)

        def process(self) -> None:
            response, error = self.download_resource(foo_txt)
            assert isinstance(response, FilePathResponse)
            assert response.payload == self._target_dir / "foo.txt"
            assert error is None
            assert (self._target_dir / "foo.txt").is_file()

    downloader2 = TestDownloader2()
    downloader2()
