import pytest

from dbnomics_fetcher_toolbox._internal.argparse_utils import csv_str


@pytest.mark.parametrize(
    ("input_value", "expected_output"),
    [
        ("", []),
        ("a", ["a"]),
        ("a,b", ["a", "b"]),
        ("a,b,c", ["a", "b", "c"]),
        ("a, b", ["a", "b"]),
        ("a ,b", ["a", "b"]),
    ],
)
def test_csv_str__valid(input_value: str, expected_output: list[str]) -> None:
    output = csv_str(input_value)
    assert output == expected_output


@pytest.mark.parametrize("input_value", [" ", ",", ", ", " ,", "a,", ",a", ",,a", "a,,"])
def test_csv_str__invalid(input_value: str) -> None:
    with pytest.raises(ValueError, match="Invalid input: "):
        csv_str(input_value)
