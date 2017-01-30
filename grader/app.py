from grader import *
from pytest_grading import *

if __name__ == "__main__":
    grader = Grader(PytestGrading)
    grader.grade_assignment("examples/assignment_tests", "examples/assignment",
                            verbose=True)
