from functools import partial
import os
from rarfile import RarFile, is_rarfile
import shutil
from zipfile import ZipFile, is_zipfile


class MoodleUnzipper():
    """
    A program to unzip Moodle-generated submission compilations for grading.
    This works by recursively unzipping the nested archives into an output
    directory. It also prints out a list of submissions that failed to extract
    in case any of the students submitted an invalid ZIP archive.
    """

    def unzip(path, output="moodle", remove_output_first=True):
        if remove_output_first is True:
            shutil.rmtree(output, ignore_errors=True)

        # Extract the Moodle zip into the output directory.
        with ZipFile(path) as overall_zip:
            overall_zip.extractall(path=output)

        failed = []
        # Walk the output and extract all the inner per-student archives.
        for inner_path in files(output):
            try:
                if is_zipfile(inner_path):
                    with ZipFile(inner_path) as inner_zip:
                        # Gets the name of the zip by stripping the extension.
                        zip_name, _ = os.path.splitext(inner_path)
                        output_path = os.path.join(output, zip_name)
                        inner_zip.extractall(path=output_path)
                elif is_rarfile(inner_path):
                    with RarFile(inner_path) as inner_rar:
                        # Gets the name of the rar by stripping the extension.
                        rar_name, _ = os.path.splitext(inner_path)
                        output_path = os.path.join(output, rar_name)
                        inner_rar.extractall(path=output_path)
            except Exception as e:
                # Failed to extract the file as a ZIP or RAR.
                failed.append(inner_path)

        # Print out failed archives.
        if len(failed) > 0:
            print("Failed to extract: {}".format(failed))

        # Return a list of directories for each student's assignments.
        results = list(dirs(output))

        # Maps subdir_if_necessary to deal with variety in ZIP format.
        return sorted(map(subdir_if_necessary, results))


def is_valid_path(path):
    """Returns true if the path is not hidden and is not a known bad path."""
    return "__MACOSX" not in path and ".idea" not in path \
        and "__pycache__" not in path and "/." not in path


def subdir_if_necessary(path):
    """
    Recursively follows subdirectories that are valid by is_valid_path. This is
    necessary to deal with variability in user submissions, as some users
    include nested directories and others do not.
    """
    subdirs = list(filter(is_valid_path, dirs(path)))
    if len(subdirs) is 0:
        return path
    else:
        return subdir_if_necessary(subdirs[0])


def files(path):
    """Gets all the files in the specified directory."""
    return filter(
        os.path.isfile, map(partial(absolutize, path), os.listdir(path))
    )


def dirs(path):
    """Gets all the directories in the specified directory."""
    return filter(
        os.path.isdir, map(partial(absolutize, path), os.listdir(path))
    )


def absolutize(base, path):
    """
    Converts the specified path into an absolute path after joining the parts.
    """
    return os.path.abspath(os.path.join(base, path))


def flatten(xs):
    """
    Flattens a nested list.

    Example: flatten([[1, 2, 3], [4], [], [5, 6]]) == [1, 2, 3, 4, 5, 6]
    """
    return [y for ys in xs for y in ys]
