from grader.moodle_unzipper import *
import pytest

not_macos_data = [
    ("foo/bar/__MACOSX",  False),
    ("a/b/blah.py",        True),
    ("blah/__MACOSX/blah", True),
    ("/foo/bar/baz",       True),
    ("blah/MACOSX",        True),
]

@pytest.mark.parametrize("path, expected", not_macos_data)
def test_is_not_macos(path, expected):
    assert is_not_macos(path) == expected


flatten_data = [
    ([[1, 2, 3], [4], [], [5, 6]], [1, 2, 3, 4, 5, 6]),
    ([[], [], [], [], []], []),
    ([["a", "b"], ["c", "d"]], ["a", "b", "c", "d"]),
    ([[[1], [2]], [[3], [4]]], [[1], [2], [3], [4]])
]

@pytest.mark.parametrize("xs, expected", flatten_data)
def test_flatten(xs, expected):
    assert flatten(xs) == expected
