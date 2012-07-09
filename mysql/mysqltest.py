#Java/SQL stuff
from java.lang import *
from java.sql import *
from java.util import Random
#from classpathhacker import classPathHacker
import com.mysql.jdbc.Driver

#Grinder stuff
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test

#misc
import time
import sys
#from random import random

#project specific
from datagenerator import TSdata

test1 = Test(1, "Database insert")
test2 = Test(2, "Database query")

#import java sql driver 
#jarLoad = classPathHacker()
#a = jarLoad.addFile("/home/test/dev/tsdb-perf-test/bin/mysql-connector-java-5.1.21-bin.jar")

def initialize_driver():
    driver = "com.mysql.jdbc.Driver"
    Class.forName(driver)

def experiment_clean():
    conn = DriverManager.getConnection(TEST_URL)
    s = conn.createStatement()
    try:
        s.executeUpdate("drop table grindertest")
    except:
        pass
    s.executeUpdate("create table grindertest (streamid INT, time INT, value DOUBLE)")
    ensureClosed(s)
    ensureClosed(conn)

def start_conn_statement():
    conn = DriverManager.getConnection(TEST_URL)
    s = conn.createStatement()
    return conn, s

def ensureClosed(object):
    try:
        object.close()
    except:
        pass

TEST_URL = "jdbc:mysql://localhost/grindertest?user=root&password=toor"

#initialize db driver
initialize_driver()
experiment_clean()
points = 10000
streams = 100
valid_range = range(80, 120, 1)
datagen = TSdata(points, streams, valid_range)

class TestRunner:
    def __init__(self):
        grinder.logger.info("Started Logging: " + str(points) + " points each for " + str(streams) + " streams at " + str(time.time()) + " seconds since the epoch.")

    def __call__(self):
        #start this round
        conn, s = start_conn_statement()
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

        ensureClosed(conn)
        ensureClosed(s)


