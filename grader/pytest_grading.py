import re

class PytestGrading():
    def grading_command():
        return "pytest"

    def assignment_path():
        return "/opt/assignment"

    def test_path():
        return PytestGrading.assignment_path() + "/test"

    def docker_image():
        return "aatxe/pytest"

    def docker_working_dir():
        return PytestGrading.assignment_path()

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
        return "{}\n{}".format(grade_line, "\n".join(output))


def group_or_else(**kwargs):
    if kwargs["match"] is not None:
        index = kwargs["group"]
        return kwargs["match"].group(index)
    else:
        return kwargs["default"]
