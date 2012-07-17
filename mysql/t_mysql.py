#Java/SQL Stuff
from java.lang import *
from java.sql import *
import com.mysql.jdbc.Driver

#misc
import time
import sys
import random

#project specific
from framework import DBTest


class MySQLAccess(DBTest):
    def __init__(self):
        #general properties
        self.db = "grindertest"
        self.urlroot = "jdbc:mysql://localhost/"
        self.dbabout = "information_schema"
        self.user = "root"
        self.passw = "toor"
        self.dbconn = None
        self.dbstate = None
        self.dbaboutconn = None
        self.dbaboutstate = None

        #setup driver
        self.driver = "com.mysql.jdbc.Driver"
        Class.forName(self.driver)
    

        #start connection/statement
        self.reset_conn_state() #THIS IS REQUIRED BEFORE self.prepare()

        #prepare the database for an experiment and create conn/state
        self.prepare()

    def reset_conn_state(self):
        if self.dbconn != None:
            #if this is called as a true reset, close the old ones
            self.close_all()


        #start connection to self.db db
        self.dbconn = DriverManager.getConnection(self.urlroot + self.db +
                                                    "?user=" + self.user + 
                                                    "&password=" + self.passw)
        self.dbstate = self.dbconn.createStatement()
    
        #start connection to information_schema db
        self.dbaboutconn = DriverManager.getConnection(self.urlroot +
                                                       self.dbabout + "?user=" +
                                                       self.user + 
                                                       "&password=" +
                                                       self.passw)
        self.dbaboutstate = self.dbaboutconn.createStatement()

        
    def close_all(self):
        self.check_close(self.dbstate)
        self.check_close(self.dbconn)
        self.check_close(self.dbaboutstate)
        self.check_close(self.dbaboutconn)

    def check_close(self, ob):
        try:
            ob.close()
        except:
            pass


    def get_db_size(self):
        size = self.dbaboutstate.executeQuery("select DATA_LENGTH from tables"
                                              " where TABLE_NAME='grindertest'")
        size.next()
        size = size.getString("DATA_LENGTH")
        return size

    def prepare(self):
        # reset the table, create if it doesn't exist
        try:
            self.dbstate.executeUpdate("drop table grindertest")
        except:
            pass
        self.dbstate.executeUpdate("create table grindertest (streamid INT,"
                                   " time INT, value DOUBLE, CONSTRAINT pk_ts"
                                   " PRIMARY KEY (streamid, time) )")
        #the end of this query creates the primary key and automatically creates 
        #an index in mysql

        ########UNCOMMENT THIS LINE TO USE InnoDB Instead of MyISAM!!!!!!!!!!!!!
        #self.dbstate.executeUpdate("ALTER TABLE grindertest ENGINE = innodb")



        #################Other things go here like clearing cache
        #clear MySQL Query Cache
        self.dbstate.executeUpdate("RESET QUERY CACHE")

        #finally, reset the connection/statement
        self.reset_conn_state()

    def run_insert_w(self):
        conn, s = self.dbconn, self.dbstate

        roundvals = self.insertGenerator.next() #potential StopIteration()
        queryend = ''
        for tup in roundvals:
            queryend += str(tup) + ','
        queryend = queryend[:-1]
        starttime = time.time()
        s.executeUpdate("insert into grindertest values " + queryend)
        endtime = time.time()
        completiontime = endtime - starttime
        return [starttime, endtime, completiontime]


    def run_query_all(self):
        conn, s = self.dbconn, self.dbstate
        starttime = time.time()
        temp = s.executeQuery("select * from grindertest")
        endtime = time.time()
        completiontime = endtime - starttime
        return [starttime, endtime, completiontime]

    def query(self, records, streams):
        """Query "records" records from "streams" streams""" 
        #ref: the bounds on between in mysql (and postgres) are inclusive
        conn, s = self.dbconn, self.dbstate

        #pick a random number between the db starttime and the greatest time
        #value - records

        #NOT PART OF timing
        temp = s.executeQuery("select max(time) as time from grindertest")
        temp.next()
        last = temp.getInt("time")
        lastpossible = last - records + 1
        default_starttime = 946684800
        starttime = random.randrange(default_starttime, lastpossible)
        endtime = starttime + records - 1
        #done random time window selection

        self.reset_conn_state()
        conn, s = self.dbconn, self.dbstate

        #build the query
        querystring = "select * from grindertest where time between "
        querystring += str(starttime) + " and " + str(endtime) + " and "
        querystring += "streamid between 1 and " + str(streams)

        #start timing
        starttime = time.time()
        temp = s.executeQuery(querystring)
        endtime = time.time()

        while temp.next():
            print(temp.getString('time'))

        completiontime = endtime - starttime
        return [starttime, endtime, completiontime]
