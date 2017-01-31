from grader import *
from moodle_unzipper import *
from pytest_grading import *

if __name__ == "__main__":
    grader = Grader(PytestGrading)
    moodle_path = "COMPSCI220-SEC01 SP17-Project 1-1234798.zip"
    test_path = "project_1/tests"
    for project_path in MoodleUnzipper.unzip(moodle_path):
        print("Grading {}".format(project_path))
        grader.grade_assignment(test_path, project_path, verbose=True)
