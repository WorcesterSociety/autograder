from grader.pytest_grading import PytestGrading
import pytest

test_data = [
    ("""========================= test session starts ========================
    platform linux -- Python 3.5.2, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
    rootdir: /vagrant, inifile: 
    collected 4 items 
    
    tests/test_grader.py ....

    ====================== 4 passed in 0.32 seconds ======================""",
     { "failed": 0, "passed": 4 }),

    ("""========================= test session starts ========================
    platform linux -- Python 3.5.2, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
    rootdir: /vagrant, inifile: 
    collected 4 items 
    
    tests/test_grader.py ....

    ================= 2 failed, 4 passed in 0.32 seconds =================""",
     { "failed": 2, "passed": 4 }),

    ("""========================= test session starts ========================
    platform linux -- Python 3.5.2, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
    rootdir: /vagrant, inifile: 
    collected 4 items 
    
    tests/test_grader.py ....

    ================= 5 failed in 0.32 seconds =================""",
     { "failed": 5, "passed": 0 }),
]

@pytest.mark.parametrize("output, expected", test_data)
def test_parse_output(output, expected):
    assert PytestGrading.parse_output(output.split("\n")) == expected
