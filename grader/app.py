#!/usr/bin/env python3
import argparse
from configparser import *
from grader import *
from moodle_unzipper import *
from name_parser import *
import os
from pytest_grading import *
import random

parser = argparse.ArgumentParser(description="Grade assignments using Docker!")

parser.add_argument(
    "test_path", type=str,
    help="the path to the desired tests for the assignment"
)

parser.add_argument(
    "zip_path", type=str,
    help="the path to the ZIP archive of assignments from Moodle or the path \
    to the individual assignment to grade"
)

parser.add_argument(
    "-p", "--positivity", type=str, nargs="?", default="positive-feedback.db",
    help="specify the path to the positive feedback database for 100% scores!"
)

parser.add_argument(
    "-db", "--dbfile", type=str, nargs="?", default="spire-ids.db",
    help="specify the database path for the student ID database."
)

parser.add_argument(
    "-o", "--outfile", type=str, nargs="?",
    help="specify the output path to a Moodle-formatted CSV"
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
    if ext != ".zip":
        grader.grade_assignment(
            args.test_path, args.zip_path, verbose=True, loud=True, timeout=30
        )
    else:
        count, total = 0, 0
        if args.outfile is not None:
            db = ConfigParser()
            db.read(args.dbfile)
            outfile = open(args.outfile, "w")
            outfile.write("ID,Grade,Feedback\n")
        for project_path in MoodleUnzipper.unzip(args.zip_path):
            grade, report = grader.grade_assignment(
                args.test_path, project_path, verbose=True, timeout=30
            )
            count += 1
            total += grade
            if outfile is not None:
                if grade == 100:
                    feedback = random.choice(open(args.positivity).readlines())
                else:
                    feedback = report
                name = parse_name(project_path)
                identifier = db["ids"][name]
                outfile.write("{},{},\"{}\"\n".format(
                    identifier, grade, feedback
                ))
        print("Average: {}".format(total / count))
        if outfile is not None:
            outfile.close()
