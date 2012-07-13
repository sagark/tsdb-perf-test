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

#test1 = Test(1, "Database insert")
#test2 = Test(2, "Database query")

class TestRunner:
    def __init__(self):
        self.testdb = DBAccess()
        self.numstreams = 5
        logstr = self.testdb.init_insert(10000, self.numstreams, False)
        grinder.logger.info(logstr)
        #setup by inserting 1,000,000 streams into self.numstreams streams
        while True:
            try:
                
                res = self.testdb.run_insert()
                grinder.logger.info("Insertion Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")

                size = self.testdb.get_db_size()
                grinder.logger.info("The database size is now " + size + 
                                                                      " bytes.")

                print("done insert")
            except StopIteration:
                # the test setup is complete
                grinder.logger.info("Insertion finished at: " + str(time.time()))
                break      
                #self.testdb.close_all()
                #grinder.stopThisWorkerThread()
        self.counter = 0

    def __call__(self):
        #start Query test
                
        self.counter += 1
        res = self.testdb.run_query_all()
        grinder.logger.info("Query     Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")

	    #log db size
        size = self.testdb.get_db_size()
        grinder.logger.info("The database size is now " + size + " bytes.")

        self.testdb.reset_conn_state()

        if self.counter > 9:
            self.testdb.close_all()
            grinder.stopThisWorkerThread()

