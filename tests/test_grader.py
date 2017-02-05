from grader.grader import Grader
import pytest

grading_data = [
    ({ "failed": 0, "passed": 10 }, 100),
    ({ "failed": 5, "passed":  5 },  50),
    ({ "failed": 3, "passed":  6 },  67),
    ({ "failed": 9, "passed":  0 },   0),
]

@pytest.mark.parametrize("res, expected", grading_data)
def test_calculate_grade(res, expected):
    assert Grader.calculate_grade(res) == expected
