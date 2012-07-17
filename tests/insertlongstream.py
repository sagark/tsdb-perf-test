#Java/SQL stuff
from java.lang import *

#Grinder stuff
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test

#misc
import time
import sys

#project specific
from framework import TSdata_w, TSdata_h, importstrs

#import relevant t_DATABASENAME depending on settings in grinder.properties
inp = grinder.getProperties()["grinder.inp"]
inp = importstrs(inp)
exec(inp)

class TestRunner:
    def __init__(self):
        self.testdb = DBAccess()
        self.numstreams = 100 
        logstr = self.testdb.init_insert(100000, self.numstreams, False)
        grinder.logger.info(logstr)
        #this has a crazy amount of overhead in python, need to figure out 
        #what's up

    def __call__(self):
        try:
            res = self.testdb.run_insert_h()
            grinder.logger.info("Insertion Results as (start time, end time, "
                        "completion" + 
                        " time): (" + str(res[0]) + ", " + str(res[1]) + 
                        ", " + str(res[2]) + ")")
            print("done insert")
        except StopIteration:
            # the test is complete
            grinder.logger.info("Insertion finished at: " + str(time.time()))    
            self.testdb.close_all()
            grinder.stopThisWorkerThread()
        

        res = self.testdb.run_query_all()
        grinder.logger.info("Query     Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")

	    #log db size
        size = self.testdb.get_db_size()
        grinder.logger.info("The database size is now " + size + " bytes.")

        self.testdb.reset_conn_state()
