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
        self.testdb = DBAccess(*dbargs)
        self.streams = 1000
        self.records = 10000
        logstr = self.testdb.init_insert(self.records, self.streams, True)
        grinder.logger.info(logstr)
        self.counter = 0

    def __call__(self):
        #start this round
        try:
            res = self.testdb.run_insert_w()
            grinder.logger.info("Insertion Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")
        except StopIteration:
            # the test is complete
            grinder.logger.info("Insertion finished at: " + str(time.time()))       
            self.testdb.close_all()
            grinder.stopThisWorkerThread()
        
        res = self.testdb.query(records=100, streams=1000)
	grinder.logger.info("Query 100 records from 1000 streams Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")


        if self.counter % 1000000 == 0:
            #run the full query test every one million records
            res = self.testdb.run_query_all()
            grinder.logger.info("Query all records Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")
	
	    #log db size
        size = self.testdb.get_db_size()
        grinder.logger.info("The database size is now " + size + " bytes.")
        self.counter += self.streams # add number of streams each time, since we're adding
	# a point to each stream every round
        self.testdb.reset_conn_state()
