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
        self.streams = 10000
        self.numpts = 100
        logstr = self.testdb.init_insert(self.numpts, self.streams, True)
        grinder.logger.info(logstr)

    def __call__(self):
        #start this round
        if self.callcounter < 100:
            self.part_one() #this is the pre/during insertion test
            if self.callcounter == 99:
                #record completion to log
                grinder.logger.info("Insertion finished at: " + str(time.time()))       

        elif self.callcounter < 200:
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
        qnumpts = self.callcounter * 10  #starts at 1000 by default
        ####NEED SOME CODE HERE TO CONTROL THE QUERY SIZE based on run #
        res = self.testdb.query(qnumpts, self.streams)
        grinder.logger.info("Query " + str(qnumpts*self.streams) + 
                            "items Results as (start time, end time, "
                            "completion" + 
                            " time): (" + str(res[0]) + ", " + str(res[1]) + 
                            ", " + str(res[2]) + ")")

        
        #the query over all streams where numstreams (qnumstreams) varies over time



        # the query over all streams getting the last x points from all streams
        # the query should go one stream at a time, like real usage


        # REQUIRED
        self.testdb.reset_conn_state()
