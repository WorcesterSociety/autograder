from functools import partial
import os
import shutil
from zipfile import ZipFile, BadZipFile


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
        # Walk the output and extract all the inner per-student zips.
        for inner_zip_path in files(output):
            try:
                with ZipFile(inner_zip_path) as inner_zip:
                    # Gets the name of the zip by stripping the .zip.
                    zip_name = inner_zip_path[:inner_zip_path.rfind(".zip")]
                    output_path = os.path.join(output, zip_name)
                    inner_zip.extractall(path=output_path)
            except BadZipFile:
                # File was not a ZIP archive, it might be RAR or something.
                failed.append(inner_zip_path)

        # Print out failed archives.
        print("Failed to extract: {}".format(failed))

        # Return a list of directories for each student's assignments.
        results = flatten(map(dirs, dirs(output))) + list(dirs(output))

        # Filters out special __MACOSX folders from macOS-made ZIP files.
        # Maps subdir_if_necessary to deal with variety in ZIP format.
        return map(subdir_if_necessary, filter(is_not_macos, results))


def is_not_macos(path):
    """Returns true if the path does not end with __MACOSX"""
    return path.endswith("__MACOSX") is False


# This function exists to deal with the high variability in ZIP formatting.
# Some submissions will be in folders, others will not.
# This helps us by recurring into the first subdirectories if they exist.
def subdir_if_necessary(path):
    """
    Recursively follows subdirectories that are not hidden and do not contain
    the word 'test'. This is necessary to deal with variability in user
    submissions, as some users include nested directories and others do not.
    """
    if len(list(dirs(path))) is 0:
        return path
    else:
        value = next(dirs(path))
        if "test" in value or "/." in value:
            return path
        else:
            return subdir_if_necessary(value)


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
