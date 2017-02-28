from functools import partial
import itertools
import re


class PytestGrading():
    """A grading behavior for grading Python assignments using Pytest."""

    def grading_command():
        """The command to run in the Docker container."""
        return "pytest test"

    def assignment_path():
        """The path to mount the assignment within the Docker container."""
        return "/opt/assignment"

    @classmethod
    def test_path(cls):
        """The path to mount the tests within the Docker container."""
        return cls.assignment_path() + "/test"

    def docker_image():
        """The desired Docker image to grade the assignment in."""
        return "aatxe/pytest"

    @classmethod
    def docker_working_dir(cls):
        """The Docker working directory to run the grading command in."""
        return cls.assignment_path()

    def parse_output(output):
        """
        Parses the output from grading to get out a dictionary with failed and
        passed test counts.
        """
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
        """Generates a feedback report to write out for the assignment."""
        grade_line = "Final Grade: {}%".format(grade)

        # Get only the lines after the last instance of test session starts.
        pytest_out = reversed_takewhile(
            lambda line: "test session starts" not in line, output
        )

        # Parse the first line (following test session starts) for information.
        info = "platform ([a-zA-Z0-9]+) -- (Python [0-9.]+), (pytest-[0-9.]+)"
        platform = re.match(info, pytest_out[0])
        info_line = "Assignment was graded on {} with {} and {}.".format(
            platform.group(1), platform.group(2), platform.group(3)
        )

        # Get only the following the FAILURES heading in the output.
        failures = reversed_takewhile(
            lambda line: "FAILURES" not in line, pytest_out
        )

        # Determine the names of failed tests from failures section of output.
        test_name = "[_]+ (test_[a-zA-Z0-9_\[\]\-]+) [_]+"
        failed = filter(not_none, map(partial(re.match, test_name), failures))

        # Generates failure report for feedback.
        failed_report = map(
            lambda x: "Failed test: {}".format(x.group(1)), failed
        )

        return "{}\n{}\n{}".format(
            grade_line, info_line, "\n".join(failed_report)
        )


# itertools.takewhile, but from the end of the list.
def reversed_takewhile(pred, xs):
    """Takes elements from the back of the list while the predicate holds."""
    return list(itertools.takewhile(pred, xs[::-1]))[::-1]


def not_none(x):
    """Returns true if the argument is not None"""
    return x is not None


def group_or_else(**kwargs):
    """
    Gets the specific regular expression group if there's a match, otherwise
    returns the specified default value.

    Keyword arguments:
    match -- the regular expression match
    group -- the index of the desired group to get
    default -- the default value to return when the match is not found
    """
    if kwargs["match"] is not None:
        index = kwargs["group"]
        return kwargs["match"].group(index)
    else:
        return kwargs["default"]
