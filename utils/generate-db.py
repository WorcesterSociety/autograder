#!/usr/bin/env python3
import argparse
import csv
import os

parser = argparse.ArgumentParser(
    description="Generates a student ID database from a Moodle gradebook CSV."
)

parser.add_argument(
    "inpath", type=str,
    help="the path to the Moodle gradebook CSV."
)

parser.add_argument(
    "outpath", type=str,
    help="the path to write the database out to."
)

parser.add_argument(
    "-v", "--verbose", action="store_true",
    help="increase verbosity by listing files as they are added to the \
    submission."
)

if __name__ == "__main__":
    args = parser.parse_args()

    with open(args.inpath) as infile:
        gradebook = csv.DictReader(infile)
        with open(args.outpath, "w") as outfile:
            outfile.write("[ids]\n")
            for row in gradebook:
                name = row["First name"] + " " + row["Last name"]
                ident = row["ID number"]
                outfile.write("{}: {}\n".format(name, ident))
                if args.verbose:
                    print("Added {} as {}".format(name, ident))

    print("Generated database to {}".format(args.outpath))
