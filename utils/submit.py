#!/usr/bin/env python3
import argparse
import os
import time
from zipfile import ZipFile

# Set up command-line argument parser.
parser = argparse.ArgumentParser(
    description="Package up your UMass COMPSCI homework for submission!"
)

parser.add_argument(
    "path", type=str, default=".", nargs="?",
    help="the path to the root of the assignment, defaults to the present \
    working directory."
)

parser.add_argument(
    "-v", "--verbose", action="store_true",
    help="increase verbosity by listing files as they are added to the \
    submission."
)

# List of file extensions to include in the submission.
included_file_extensions = [".py"]

if __name__ == "__main__":
    args = parser.parse_args()

    # Generate a timestamped file name for the submission.
    zip_file_name = time.strftime(
        "submission-%m-%d-%Y-%H-%M-%S.zip", time.localtime()
    )

    # Build submission by walking directory.
    with ZipFile(zip_file_name, "w") as submission:
        for dir_path, _, file_names in os.walk(args.path):
            for file_name in file_names:
                _, ext = os.path.splitext(file_name)
                if ext in included_file_extensions:
                    file_path = os.path.join(dir_path, file_name)
                    submission.write(file_path)
                    if args.verbose:
                        print("Added {}".format(file_name))

    print("Generated submission as {}".format(zip_file_name))
    print("Please submit this file to Moodle.")
