import os
import string

# A magic constant that occurs in all official Moodle submission names.
magic = "assignsubmission"

# Parses the person's name from their project path, given the Moodle path
# format.
def parse_name(path):
    pieces = path.split(os.path.sep)
    dir_name = next(piece for piece in pieces if magic in piece)
    name = dir_name[:dir_name.find("_")]
    return name
