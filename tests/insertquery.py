#Java/SQL stuff
from java.lang import *

#Grinder stuff
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test

#misc
import time
import sys

#project specific
from framework import TSdata, importstrs

#import relevant t_DATABASENAME depending on settings in grinder.properties
inp = grinder.getProperties()["grinder.inp"]
inp = importstrs(inp)
exec(inp)

test1 = Test(1, "Database insert")
test2 = Test(2, "Database query")

class TestRunner:
    def __init__(self):
        self.testdb = DBAccess()
        logstr = self.testdb.init_insert(100, 10000)
        grinder.logger.info(logstr)

    def __call__(self):
        #start this round
        try:
            res = self.testdb.run_insert()
            grinder.logger.info("Results as (start time, end time, completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")
        except StopIteration:
            # the test is complete
            grinder.logger.info("Insertion finished at: " + str(time.time()))       
            self.testdb.close_all()
            grinder.stopThisWorkerThread()
        

        res = self.testdb.run_query_all()
        grinder.logger.info("Results as (start time, end time, completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")

	    #log db size
        size = self.testdb.get_db_size()
        grinder.logger.info("The database size is now " + size + " bytes.")

        self.testdb.reset_conn_state()


