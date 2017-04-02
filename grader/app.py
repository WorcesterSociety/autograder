#!/usr/bin/env python3
import argparse
from grader import *
from moodle_unzipper import *
import os
from pytest_grading import *

parser = argparse.ArgumentParser(description="Grade assignments using Docker!")

parser.add_argument(
    "test_path", type=str,
    help="the path to the desired tests for the assignment"
)

parser.add_argument(
    "zip_path", type=str,
    help="the path to the ZIP archive of assignments from Moodle or the path to the individual assignment to grade"
)

parser.add_argument(
    "-py", "--python", help="grade assignments written in Python using pytest",
    dest="grading_behavior", action="store_const", const=PytestGrading,
    default=PytestGrading
)

if __name__ == "__main__":
    args = parser.parse_args()
    grader = Grader(args.grading_behavior)
    _, ext = os.path.splitext(args.zip_path)
    if ext != "zip":
        grader.grade_assignment(args.test_path, args.zip_path, verbose=True, timeout=30)
    else:
        for project_path in MoodleUnzipper.unzip(args.zip_path):
            grader.grade_assignment(args.test_path, project_path, verbose=True, timeout=30)
