from grader.name_parser import parse_name
import pytest

test_data = [
    ("moodle/Example Man_958105_assignsubmission_file_Project", "Example Man"),
    ("moodle/Ex Ample Man_958105_assignsubmission_file_Project", "Ex Ample Man"),
    ("moodle/Example Man_958105_assignsubmission_file_Project/foobar_proj_Example_Man", "Example Man")
]

@pytest.mark.parametrize("output, expected", test_data)
def test_parse_output(output, expected):
    assert parse_name(output) == expected
