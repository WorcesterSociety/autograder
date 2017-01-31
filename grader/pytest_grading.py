from functools import partial
import itertools
import re


class PytestGrading():
    def grading_command():
        return "pytest"

    def assignment_path():
        return "/opt/assignment"

    @classmethod
    def test_path(cls):
        return cls.assignment_path() + "/test"

    def docker_image():
        return "aatxe/pytest"

    @classmethod
    def docker_working_dir(cls):
        return cls.assignment_path()

    def parse_output(output):
        failing = "([0-9]+) failed"
        passing = "([0-9]+) passed"

        failed = re.search(failing, output[-1])
        passed = re.search(passing, output[-1])

        # Group 1 corresponds to the numeric portion of both matches.
        return {
            "failed": int(group_or_else(match=failed, group=1, default=0)),
            "passed": int(group_or_else(match=passed, group=1, default=0)),
        }

    def generate_report(grade, output):
        grade_line = "Final Grade: {}%".format(grade)

        # Get only the lines following the last instance of test session starts
        pytest_out = reversed_takewhile(
            lambda line: "test session starts" not in line, output
        )

        # Get only the following the FAILURES heading in the output.
        failures = reversed_takewhile(
            lambda line: "FAILURES" not in line, pytest_out
        )

        # Determine the names of failed tests from failures section of output.
        regex = "[_]+ (test_[a-zA-Z0-9_]+) [_]+"
        failed = filter(not_none, map(partial(re.match, regex), failures))

        # Generates failure report for feedback.
        failed_report = map(
            lambda x: "Failed test: {}".format(x.group(1)), failed
        )

        return "{}\n{}".format(grade_line, "\n".join(failed_report))


# itertools.takewhile, but from the end of the list.
def reversed_takewhile(pred, xs):
    return list(itertools.takewhile(pred, xs[::-1]))[::-1]


def not_none(x):
    return x is not None


def group_or_else(**kwargs):
    if kwargs["match"] is not None:
        index = kwargs["group"]
        return kwargs["match"].group(index)
    else:
        return kwargs["default"]
