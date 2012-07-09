# a jython script for use by grinder
#import warnings
#warnings.filterwarnings("ignore", category=PendingDeprecationWarning)


#Java/SQL stuff
from java.lang import *
from java.sql import *
from java.util import Random
from classpathhacker import classPathHacker
#import com.mysql.jdbc.Driver

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
jarLoad = classPathHacker()
a = jarLoad.addFile("../bin/mysql-connector-java-5.1.21-bin.jar")

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
    s.executeUpdate("create table grindertest (time INT, value DOUBLE)")
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



#random numbergen
r = Random()

TEST_URL = "jdbc:mysql://localhost/grindertest?user=root&password=toor"

#initialize db driver
initialize_driver()
experiment_clean()


class TestRunner:
    def __call__(self):
        r = Random()

        conn, s = start_conn_statement()

        testInsert = test1.wrap(s)
        testInsert.executeUpdate("insert into grindertest values (" + 
                      str(int(time.time())) + "," + str(r.nextInt(100)) + ")")
        
        testQuery = test2.wrap(s)
        a = testQuery.executeQuery("select * from grindertest")
        while(a.next()):
            print("[" + a.getString("time") + " " + a.getString("value") + "]")

        ensureClosed(conn)
        ensureClosed(s)


