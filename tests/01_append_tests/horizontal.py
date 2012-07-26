#based off of insertquery.py

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
        self.callcounter = 0
        self.testdb = DBAccess()

        self.streams = 100 #number of streams
        self.numpts = 300 #number of points per stream
        self.callcountermax = self.numpts #set counter for loop

        self.qnumpts = 100 #smallest query size
        self.qnumptsmax = 300 #largest query size
        self.qnumptsinc = 10 #query size increment

        self.callcounter_q_max = (self.qnumptsmax - self.qnumpts)/self.qnumptsinc

        logstr = self.testdb.init_insert(self.numpts, self.streams, True)
        grinder.logger.info(logstr)

    def __call__(self):
        #start this round
        print("run #" + str(self.callcounter))
        if self.callcounter < self.callcountermax:
            self.part_one() #this is the pre/during insertion test
            if self.callcounter == (self.callcountermax-1):
                #record completion to log
                grinder.logger.info("Insertion finished at: " + str(time.time()))       

        elif self.callcounter < (self.callcountermax + self.callcounter_q_max):
            self.part_two() #this is the post insertion test

        else:
            self.testdb.close_all()
            grinder.stopThisWorkerThread()
        self.callcounter += 1



    def part_one(self):
        res = self.testdb.run_insert_w()
        grinder.logger.info("Insertion Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")
                    

        res = self.testdb.run_query_all()
        grinder.logger.info("Query     Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")

	    #log db size
        size = self.testdb.get_db_size()
        grinder.logger.info("The database size is now " + size + " bytes.")

        self.testdb.reset_conn_state()


    def part_two(self):
        #the control query
        res = self.testdb.run_query_all()
        grinder.logger.info("Control Query Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")


        #the query over all streams where numpts (qnumpts) varies over time
        #qnumpts = self.callcounter * 10  #starts at 1000 by default
        ####NEED SOME CODE HERE TO CONTROL THE QUERY SIZE based on run #
        res = self.testdb.query(self.qnumpts, self.streams)
        grinder.logger.info("Query " + str(self.qnumpts*self.streams) + 
                            " items Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")
        self.qnumpts += self.qnumptsinc

        
        #the query over all streams where numstreams (qnumstreams) varies over time



        # the query over all streams getting the last x points from all streams
        # the query should go one stream at a time, like real usage


        # REQUIRED
        self.testdb.reset_conn_state()
