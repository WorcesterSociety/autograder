import docker
import os
import signal
import time

try:
    from sh import systemctl
    restart_docker = True
except ImportError:
    # Does not use systemctl, and thus we cannot restart Docker.
    restart_docker = False

class Grader():
    """A testing infrastructure for automatically grading homework assignments.
       Uses Docker internally, and thus requires a running Docker server."""
    client = docker.from_env()

    def __init__(self, grading_behavior):
        self.grading_behavior = grading_behavior

    def grade_assignment(self, test_path, assignment_path, **kwargs):
        """Grades an assignment given the specified arguments.

        Arguments:
        test_path -- the path to the tests to use
        assignment_path -- the path to the assignment to grade

        Keyword arguments:
        verbose -- whether or not to have verbose output from grading
        """
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
        container = client.containers.create(
            image, working_dir=working_dir, command=cmd, volumes=volumes
        )

        container.start()

        try:
            # Set up timeout handler.
            signal.signal(signal.SIGALRM, Grader.handle_timeout)

            # Set alarm for timeout in seconds.
            if "timeout" in kwargs.keys():
                signal.alarm(kwargs["timeout"])

            logs = container.logs(stdout=True, stderr=True, stream=True)
            output = [line.decode("utf-8") for line in logs]

            # Reset alarm if execution completed in time.
            signal.alarm(0)

            # Parse output for a result dictionary.
            # Expecting failed and passed keys in dictionary.
            results = self.grading_behavior.parse_output(output)
            grade = Grader.calculate_grade(results)

            try:
                container.stop()
            except:
                if restart_docker:
                    systemctl.restart("docker")
                    time.sleep(3)

            # Generates a report from the output and writes it to disk.
            report = self.grading_behavior.generate_report(grade, output)
            feedback_path = assignment_path + "/feedback.txt"
            Grader.write_report(feedback_path, report)

            # Output full output in loud mode.
            if "loud" in kwargs.keys() and kwargs["loud"] is True:
                for line in output:
                    print(line)

            # Output grades in verbose mode.
            if "verbose" in kwargs.keys() and kwargs["verbose"] is True:
                print("{} received a grade of {}%.".format(
                    assignment_path, grade
                ))

            return grade, report
        except ZeroDivisionError:
            if "verbose" in kwargs.keys() and kwargs["verbose"] is True:
                print("Failed to grade {}".format(assignment_path))
            Grader.write_report(assignment_path + "/failed.txt", "\n".join(output))
            return 0, output
        except ContainerTimeout:
            container.kill()
            if "verbose" in kwargs.keys() and kwargs["verbose"] is True:
                print("Timed out while grading {}".format(assignment_path))
            return 0, "Timed out."

    def calculate_grade(results):
        """Calculates a grade from a dictionary with passed and failed keys."""
        total = results["passed"] + results["failed"]
        return int(round(results["passed"] * 100 / total))

    def write_report(feedback_path, report):
        """Writes out a grading report to the specified path."""
        with open(feedback_path, "w") as feedback:
            feedback.write(report)

    def handle_timeout(signum, frame):
        raise ContainerTimeout()

class ContainerTimeout(Exception):
    def __init__(self):
        super(ContainerTimeout, self).__init__("A timeout occurred during grading.")
