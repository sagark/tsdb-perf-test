#Java/SQL stuff
from java.lang import *
from java.sql import *
import com.mysql.jdbc.Driver

#Grinder stuff
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test

#misc
import time
import sys

#project specific
from datagenerator import TSdata
#from outline import DBTest
from t_mysql import MySQLAccess

test1 = Test(1, "Database insert")
test2 = Test(2, "Database query")


#def initialize_driver():
#    driver = "com.mysql.jdbc.Driver"
#    Class.forName(driver)
#
#def experiment_clean():
#   conn = DriverManager.getConnection(TEST_URL)
#    s = conn.createStatement()
#    try:
#        s.executeUpdate("drop table grindertest")
#    except:
#        pass
#    s.executeUpdate("create table grindertest (streamid INT, time INT, value DOUBLE)")
#    ensureClosed(s)
#    ensureClosed(conn)
#
#def start_conn_statement(turl):
#    conn = DriverManager.getConnection(turl)
#    s = conn.createStatement()
#    return conn, s
#
#def ensureClosed(object):
#    try:
#        object.close()
#    except:
#        pass

#TEST_URL = "jdbc:mysql://localhost/grindertest?user=root&password=toor"
#DB_STATS_URL = "jdbc:mysql://localhost/information_schema?user=root&password=toor"

#initialize db driver
#initialize_driver()
#experiment_clean()
points = 10000
streams = 100
valid_range = range(80, 120, 1)
datagen = TSdata(points, streams, valid_range)

class TestRunner:
    def __init__(self):
        grinder.logger.info("Started Logging: " + str(points) + " points each for " + str(streams) + " streams at " + str(time.time()) + " seconds since the epoch.")
        self.testdb = MySQLAccess()
        self.testdb.clean_for_experiment()



    def __call__(self):
        #start this round
        conn, s = self.testdb.dbconn, self.testdb.dbstate
        logconn, logstate = self.testdb.dbaboutconn, self.testdb.dbaboutstate

        roundvals = datagen.next()
        testInsert = test1.wrap(s)
        testQuery = test2.wrap(s)

        query_end = ''
        for tup in roundvals:
                query_end += str(tup) + ','
        query_end = query_end[:-1]
        testInsert.executeUpdate("insert into grindertest values " + query_end)
        grinder.logger.info("Added " + str(streams) + " points at " + str(time.time()))
        

        a = testQuery.executeQuery("select * from grindertest")
        while(a.next()):
            temp = ("[" + a.getString("streamid") + " " + a.getString("time") + " " + a.getString("value") + "]") #no need to waste time actually printing
        grinder.logger.info("Fetched all points at " + str(time.time()))


	    #log db size
        size = logstate.executeQuery("select DATA_LENGTH from tables where TABLE_NAME='grindertest'")
        size.next()
        size = size.getString("DATA_LENGTH")
        grinder.logger.info("The database size is now " + size + " bytes.")

        self.testdb.reset_conn_state()

