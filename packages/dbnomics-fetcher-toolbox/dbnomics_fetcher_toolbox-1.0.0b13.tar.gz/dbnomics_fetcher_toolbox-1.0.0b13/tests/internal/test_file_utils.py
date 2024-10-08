from collections.abc import Callable
from contextlib import _GeneratorContextManager
from pathlib import Path

from humanfriendly.text import pluralize
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from dbnomics_fetcher_toolbox.formatters import format_file_path_with_size


@given(text=st.text(min_size=0, max_size=1000))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_format_file_path_with_size(
    text: str, make_tmp_file: Callable[[str | bytes], _GeneratorContextManager[Path]]
) -> None:
    with make_tmp_file(text) as file_path:
        s = format_file_path_with_size(file_path)
        size = file_path.stat().st_size
        size_str = pluralize(size, "byte")
        assert s == f"{str(file_path)!r} ({size_str})"
