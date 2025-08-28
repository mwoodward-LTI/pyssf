import contextlib
import os

import pytest

from pyssf import SSFFormatter

formatter = SSFFormatter()


def read_test_cases():
    test_cases = []
    test_file_path = os.path.join(os.path.dirname(__file__), "tests.tsv")
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
    assert formatter.format(fmt_string, value) == expected
