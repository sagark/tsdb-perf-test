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
        self.t1size = 0 #size of query for first non-control test
        self.streams = 10 #number of streams
        self.pps = 20000 #points per stream
        logstr = self.testdb.init_insert(self.pps, self.streams, False)
        grinder.logger.info(logstr)
        self.callcounter = 0 #start the test callcounter
        counter = 0
        #prepare by inserting large number of points
        while True:
            try:
                print("inserting round: " + str(counter))
                res = self.testdb.run_insert_h()
                grinder.logger.info("Insertion Results as (start time, end time, "
                                "completion" + 
                                " time): (" + str(res[0]) + ", " + str(res[1]) + 
                                ", " + str(res[2]) + ")")
                size = self.testdb.get_db_size()
                grinder.logger.info("The database size is now " + size + " bytes.")

                self.testdb.reset_conn_state()
                counter += 1
            except StopIteration:
                # the prep is complete
                grinder.logger.info("Insertion finished at: " + str(time.time())) 
                size = self.testdb.get_db_size()
                grinder.logger.info("The database size is now " + size + " bytes.")
                self.testdb.reset_conn_state()
                break

    def __call__(self):
        if self.callcounter >= 100:
            grinder.logger.info("Test complete")
            self.testdb.close_all()
            grinder.stopThisWorkerThread()

        else:
            self.callcounter += 1 
            self.t1size += 10
        #start this round

        # this is the control. If the time that this takes varies, we know that
        # external factors are affecting our results.
        res = self.testdb.run_query_all()
        grinder.logger.info("Control Query Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")


        # actual experiment. the values for this will vary over time
        # this represents querying for data from an arbitrary time window of
        # fixed width
        # measure performance vs query size
        res = self.testdb.query(self.t1size, self.streams)
        grinder.logger.info("Query " + str(self.t1size) + " items Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")

        # actual experiement. the values for this will vary over time.
        # this represents querying for the last x values for the stream, which
        # is very common



        # reset the connection and statement
        self.testdb.reset_conn_state()
