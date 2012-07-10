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
print(inp)
inp = importstrs(inp)
exec(inp)

test1 = Test(1, "Database insert")
test2 = Test(2, "Database query")

class TestRunner:
    def __init__(self):
        self.testdb = DBAccess()
        self.points = 10000
        self.streams = 100
        self.valid_range = range(80, 120, 1)
        self.datagen = TSdata(self.points, self.streams, self.valid_range)
        grinder.logger.info("Started Logging: " + str(self.points) + 
                            " points each for " + str(self.streams) + 
                            " streams at " + str(time.time()) + 
                            " seconds since the epoch.")

    def __call__(self):
        #start this round
        conn, s = self.testdb.dbconn, self.testdb.dbstate
        logconn, logstate = self.testdb.dbaboutconn, self.testdb.dbaboutstate

        roundvals = self.datagen.next()
        testInsert = test1.wrap(s)
        testQuery = test2.wrap(s)

        query_end = ''
        for tup in roundvals:
                query_end += str(tup) + ','
        query_end = query_end[:-1]
        testInsert.executeUpdate("insert into grindertest values " + query_end)
        grinder.logger.info("Added " + str(self.streams) + " points at " + 
                                                               str(time.time()))
        

        a = testQuery.executeQuery("select * from grindertest")
        while(a.next()):
            temp = ("[" + a.getString("streamid") + " " + a.getString("time") + 
                    " " + a.getString("value") + "]") 
        #no need to waste time actually printing


        grinder.logger.info("Fetched all points at " + str(time.time()))


	    #log db size
        size = self.testdb.get_db_size()
        grinder.logger.info("The database size is now " + size + " bytes.")

        self.testdb.reset_conn_state()


