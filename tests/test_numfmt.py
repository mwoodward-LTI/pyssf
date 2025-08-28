import contextlib
from pathlib import PurePath

import pytest

from pyssf import SSFFormatter


def read_test_cases():
    test_cases = []
    test_file_path = PurePath(__file__).parent / "tests.tsv"
    with open(test_file_path) as f:
        for line in f:
            if line.rstrip("\n") and not line.startswith("~"):
                parts = line.rstrip("\n").split("\t")
                if len(parts) == 3:
                    # try to convert value to float, if it fails, it's a string
                    with contextlib.suppress(ValueError):
                        parts[1] = float(parts[1])
                    test_cases.append(parts)
    return test_cases


@pytest.mark.parametrize("fmt_string,value,expected", read_test_cases())
def test_numfmt(fmt_string, value, expected):
    formatter = SSFFormatter()
    assert formatter.format(fmt_string, value) == expected


@pytest.mark.parametrize("fmt_string,value,expected", [["0.00", 1.5555, "1.56"]])
def test_ts_path(fmt_string, value, expected):
    rel_ts_path = "vendor/main.ts"
    formatter = SSFFormatter(deno_script_path=rel_ts_path)
    assert formatter.format(fmt_string, value) == expected
