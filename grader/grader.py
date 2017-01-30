import docker
import os
import re

client = docker.from_env()


def grade_assignment(test_path, assignment_path):
    abs_assignment_path = os.path.abspath(assignment_path)
    abs_test_path = os.path.abspath(test_path)
    volumes = {
        abs_assignment_path: {'bind': '/opt/assignment', 'mode': 'rw'},
        abs_test_path: {'bind': '/opt/assignment/test', 'mode': 'ro'},
    }
    container = client.containers.create("aatxe/pytest", command="pytest",
                                         working_dir="/opt/", volumes=volumes)
    container.start()

    logs = container.logs(stdout=True, stderr=True, stream=True)
    output = [line.decode("utf-8") for line in logs]

    grade = grade_output(output)

    container.stop()

    write_output(output, grade, assignment_path, "feedback.txt")
    print("{} received a grade of {}%.".format(assignment_path, grade))


def write_output(output, grade, path, name):
    with open(path + "/" + name, "w") as feedback:
        feedback.write("Final Grade: {}%\n".format(grade))
        for line in output:
            feedback.write("{}\n".format(line))


def grade_output(output):
    last_line = output[-1]
    results = parse_pytest_line(last_line)
    total = results["passed"] + results["failed"]
    return results["passed"] * 100 / total


def parse_pytest_line(line):
    failing = "([0-9]+) failed"
    passing = "([0-9]+) passed"

    failed = re.search(failing, line)
    passed = re.search(passing, line)

    # Group 1 corresponds to the numeric portion of both matches.
    return {
        "failed": int(group_or_else(match=failed, group=1, default=0)),
        "passed": int(group_or_else(match=passed, group=1, default=0)),
    }


def group_or_else(**kwargs):
    if kwargs["match"] is not None:
        index = kwargs["group"]
        return kwargs["match"].group(index)
    else:
        return kwargs["default"]


if __name__ == "__main__":
    grade_assignment("examples/assignment_tests", "examples/assignment")
