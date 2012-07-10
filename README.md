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
-------
### /DatabaseName/

    These are folders specific to each database being tested. Each contains a
    t_databasename.py file that extends DBtest from framework.py in root. 
    This abstracts away the database queries, setup, etc. for the tests.
    
    Each folder also contains a symlink to each type of test from /tests/, a
    grinder.properties file for configuring/selecting tests.

    Finally, each folder contains a first_run file that describes first-time db
    setup instructions.

### /bin/

    Contains db drivers

### /tests/

    Contains the various tests

Files
-----
### framework.py
    
    This contains code for generating timeseries data, a pseudo-interface 
    (zope.interface doesn't work in jython) for the database abstractions, and
    an importer function that handles arguments passed at commandline (see
    grinder.properties file).

### setupguide
    
    This documents jython + grinder setup in linux.

Running Tests
=============

cd into the folder for the DB you wish to test, set the script in
grinder.properties and run:

Start the console:
java net.grinder.Console

Start the agent/process:
java net.grinder.Grinder
