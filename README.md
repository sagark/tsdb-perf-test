tsdb-perf-test
==============

Performance Tests for Time Series Databases


Setting up Grinder
==================

See setupguide

Folder Structure
================

Because I didn't want to waste even more time dealing with jython and grinder's
path system, I instead resorted to symlinks. Here's a breakdown of where things
are, starting from project root:

Folders
/<DBNAME>/
    These are folders specific to each database being tested. Each contains a
    t_databasename.py file that extends outline.py in root. This abstracts away
    the database queries, setup, etc. for the tests.
    
    Each folder also contains a symlink to each type of test from /tests/, a
    grinder.properties file for configuring/selecting tests and a symlink to
    datagenerator.py (in root).

    Finally, each folder contains a first_run file that describes first-time db
    setup instructions.

/bin/
    Contains db drivers

/tests/
    Contains the various tests

Running Tests
=============

cd into the folder for the DB you wish to test, set the script in
grinder.properties and run:

Start the console:
java net.grinder.Console

Start the agent/process:
java net.grinder.Grinder
