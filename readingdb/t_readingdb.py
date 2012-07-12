#Java/SQL Stuff
from java.lang import *

#misc
import time
import sys
import subprocess

#project specific
from framework import DBTest


class ReadingDBAccess(DBTest):
    def __init__(self):
        """For reading db, these properties are defined in the 'driver'"""
        #general properties
        #self.db = "grindertest"
        #self.urlroot = "jdbc:mysql://localhost/"
        #self.dbabout = "information_schema"
        #self.user = "root"
        #self.passw = "toor"
        #self.dbconn = None
        #self.dbstate = None
        #self.dbaboutconn = None
        #self.dbaboutstate = None

        #setup driver
        self.driver = "readingdb_drv/reading.py"
    

        #start connection/statement
        
        self.reset_conn_state() #THIS IS REQUIRED BEFORE self.prepare()

        #prepare the database for an experiment and create conn/state
        self.prepare()

    def reset_conn_state(self):
        #does nothing for readingdb
        pass

        
    def close_all(self):
        #does nothing for readingdb
        pass


    def check_close(self, ob):
        #does nothing for readingdb
        pass

    def get_db_size(self):
        #######################Need to figure out what goes here.
        size = 0
        return str(size)

    def prepare(self):
        #does nothing for readingdb
        pass

    def run_insert(self):
        #generate and store values to file
        roundvals = self.insertGenerator.next() #potential StopIteration()
        tempfile = file('tempdata', 'w')
        tempfile.write(str(roundvals))
        tempfile.close()

        #generate and store code to file, ANY CODE HERE WILL BE INCLUDED IN THE
        #TIME MEASUREMENT!
        codefile = file('tempcode', 'w')
        execcode = """
for val in roundvals:
    rdb.db_add(a, val[0], [(val[1], 0, val[2])])
        """
        codefile.write(execcode)
        codefile.close()

        #call the "driver"
        a = subprocess.call([self.driver])

        #get the time taken list from file
        timetaken = file('timetaken')
        returnlist = eval(timetaken.read())
        timetaken.close()
        return returnlist


    def run_query_all(self):
        codefile = file('tempcode', 'w')
        execcode = """
rdb.db_query(list(range(0, 1000)), 0, 10000000000)
        """
        codefile.write(execcode)
        codefile.close()

        a = subprocess.call([self.driver])
        
        timetaken = file('timetaken')
        returnlist = eval(timetaken.read())
        timetaken.close()

        return returnlist
        
