# AutoGrader [![Build Status](https://travis-ci.org/WorcesterSociety/autograder.svg?branch=master)](https://travis-ci.org/WorcesterSociety/autograder) #

An automated grading tool.

## Getting Started ##

In order to use the grader, you'll need [Docker](http://docker.com) and
[Python 3](https://www.python.org). You'll also need the command-line utility `unrar` installed. To
install these on Ubuntu, you can run the `vagrant.sh` script. Otherwise, you can use
[Vagrant](https://www.vagrantup.com) to start a virtula machine with the initial setup complete.

## Grading Assignments ##

To grade an individual assignment, you can use the following command:

```
./grader/app.py path/to/tests path/to/assignment/root
```

To grade a Moodle-exported assignment archive, you can use the following command:

```
./grader/app.py path/to/tests path/to/assignments.zip
```

To grade a Moodle-exported archive and produce an importable CSV, you can use the following command:

```
./grader/app.py path/to/tests path/to/assignments.zip -o output.csv
```

However, you should note that producing an output.csv requires a student ID database that can be
built using the `generate-db.py` script in `utils` as well as a positive feedback database
consisting of one or more line-separated responses to grades of 100%. The default paths for these
databases are `spire-ids.db` and `positive-feedback.db` respectively.

## License ##

You can find the exact details of the license in `LICENSE.md`, but this project is licensed under
the GNU Public License (GPL). The general gist is that all changes to this project must themselves
be open source.
