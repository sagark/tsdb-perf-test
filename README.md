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
    t_databasename.py file that extends DBtest from the symlinked framework.py 
    in root. This abstracts away the database queries, setup, etc. for the 
    tests.
    
    Each folder also contains a symlink to each type of test from /tests/, a
    grinder.properties file for configuring/selecting tests, and a first_run 
    file that describes first-time db setup instructions.

    Finally, the logs folder contains logs from whichever test was run last. 
    Official logs can be found in /results/.

### /bin/

    Contains db drivers

### /logparse/
    
    Contains the logfile parser and graph-maker and whatever test.png it 
    outputted last.

### /results/
    
    Contains folders formatted as NUMBER_testtype_further_description that 
    contain logs and graphs for "official" tests.

### /tests/

    Contains the various tests. They should be database-independent.

Files
-----
### framework.py
    
    This contains code for generating timeseries data, a pseudo-interface 
    (zope.interface doesn't work in jython) for the database abstractions, and
    an importer function that handles arguments passed at commandline (see
    grinder.properties file).

### README.md

    This file.

### setupguide
    
    This documents jython + grinder setup in linux.

Running Tests
=============

cd into the folder for the DB you wish to test, set the script in
grinder.properties and run:

Start the console: (Not necessary)
java net.grinder.Console

Start the agent/process: (The actual test)
java net.grinder.Grinder

Processing Results
==================

Once you have logs, copy them to a logs folder in the folder for your test in 
/results/. You should name them like so: mysql-myisam.log, mysql-innodb.log, 
postgres.log, etc. (they should match the db foldernames in root). This naming
is important because it allows the logparser to automatically generate the
legend. 

To create the graph, do:

    python logparser.py PATHTO_FIRST_LOG PATHTO_SECOND_LOG # and so on

NOTE: The current implementation of logparser will require modification for 
custom tests.

After running this, an output called test.png should be available in the 
/logparse/ folder. If the graph is as expected, copy it to your results folder
and commit.
