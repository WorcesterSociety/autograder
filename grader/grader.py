import docker
import os


class Grader():
    client = docker.from_env()

    def __init__(self, grading_behavior):
        self.grading_behavior = grading_behavior

    def grade_assignment(self, test_path, assignment_path, **kwargs):
        # Set up bind volumes for Docker.
        abs_assignment_path = os.path.abspath(assignment_path)
        abs_test_path = os.path.abspath(test_path)
        bound_assignment_path = self.grading_behavior.assignment_path()
        bound_test_path = self.grading_behavior.test_path()
        volumes = {
            abs_assignment_path: {'bind': bound_assignment_path, 'mode': 'rw'},
            abs_test_path: {'bind': bound_test_path, 'mode': 'ro'},
        }

        # Create a specific Docker container using the grading behavior.
        client = Grader.client
        image = self.grading_behavior.docker_image()
        working_dir = self.grading_behavior.docker_working_dir()
        cmd = self.grading_behavior.grading_command()
        container = client.containers.create(image, working_dir=working_dir,
                                             command=cmd, volumes=volumes)

        container.start()

        logs = container.logs(stdout=True, stderr=True, stream=True)
        output = [line.decode("utf-8") for line in logs]

        try:
            # Parse output for a result dictionary.
            # Expecting failed and passed keys in dictionary.
            results = self.grading_behavior.parse_output(output)
            grade = Grader.calculate_grade(results)

            container.stop()

            # Generates a report from the output and writes it to disk.
            report = self.grading_behavior.generate_report(grade, output)
            feedback_path = assignment_path + "/feedback.txt"
            Grader.write_report(feedback_path, report)

            # Output grades in verbose mode.
            if "verbose" in kwargs.keys() and kwargs["verbose"] is True:
                print("{} received a grade of {}%.".format(
                    assignment_path, grade
                ))
        except ZeroDivisionError:
            if "verbose" in kwargs.keys() and kwargs["verbose"] is True:
                print("Failed to grade {}".format(assignment_path))

    def calculate_grade(results):
        total = results["passed"] + results["failed"]
        return int(results["passed"] * 100 / total)

    def write_report(feedback_path, report):
        with open(feedback_path, "w") as feedback:
            feedback.write(report)
