# a jython script for use by grinder

#Java/SQL stuff
from java.lang import *
from java.sql import *
from classpathhacker import classPathHacker
#import com.mysql.jdbc.Driver

#Grinder stuff
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test

#misc
import time
import sys

test1 = Test(1, "Database insert")
test2 = Test(2, "Database query")

#import java sql driver 
jarLoad = classPathHacker()
a = jarLoad.addFile("/usr/share/java/mysql-connector-java-5.1.16.jar")

TEST_URL = "jdbc:mysql://localhost/grindertest?user=root&password=toor"

def ensureClosed(object):
    try:
        object.close()
    except:
        pass


class TestRunner:
    def __call__(self):
        driver = "com.mysql.jdbc.Driver"
        Class.forName(driver)

        conn = DriverManager.getConnection(TEST_URL)
        s = conn.createStatement()

        testInsert = test1.wrap(s)
        testInsert.executeUpdate("insert into grindertest values (%d, 1)" %
                                                               int(time.time()))
        
        testQuery = test2.wrap(s)
        a = testQuery.executeQuery("select * from grindertest")
        while(a.next()):
            print("[" + a.getString("time") + " " + a.getString("value") + "]")

        ensureClosed(conn)
        ensureClosed(s)


