from collections.abc import Callable
from contextlib import _GeneratorContextManager
from pathlib import Path

import pytest

from dbnomics_fetcher_toolbox.formats.mime import detect_mimetype, normalize_mimetype

sources = [
    "foo",
    "a,b\n0,1",
    "a\tb\n0\t1",
    "<test/>",
]


@pytest.mark.parametrize("source", sources)
def test_detect_mimetype(source: str, make_tmp_file: Callable[[str | bytes], _GeneratorContextManager[Path]]) -> None:
    expected_mimetype = "text/plain"

    detected_mimetype = detect_mimetype(source)
    assert detected_mimetype == expected_mimetype

    with make_tmp_file(source) as tmp_file:
        detected_mimetype = detect_mimetype(tmp_file)
        assert detected_mimetype == expected_mimetype


@pytest.mark.parametrize(
    ("mimetype", "expected_normalized_mimetype"),
    [
        ("text/plain", "text/plain"),
        ("text/plain; charset=charset=us-ascii", "text/plain"),
    ],
)
def test_normalize_mimetype(mimetype: str, expected_normalized_mimetype: str) -> None:
    normalized_mimetype = normalize_mimetype(mimetype)
    assert normalized_mimetype == expected_normalized_mimetype
