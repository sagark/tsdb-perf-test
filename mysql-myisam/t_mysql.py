#IMPORTANT: This is shared between mysql-myisam and mysql-innodb. The "real"
#file resides in the mysql-myisam directory

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
from dbconfig import DBconfig

class MySQLAccess(DBTest):
    def __init__(self, engine):
        #general properties
        self.db = DBconfig.db
        self.urlroot = "jdbc:mysql://localhost/"
        self.dbabout = DBconfig.dbabout
        self.user = DBconfig.user
        self.passw = DBconfig.passw
        self.dbconn = None
        self.dbstate = None
        self.dbaboutconn = None
        self.dbaboutstate = None
        self.engine = engine

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
        self.dbstate.setQueryTimeout(100000) #fixes timeout errors

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
        #the end of this query creates the primary key and automatically creates 
        #an index in mysql

        ###Select engine based on self.engine obtained from grinder.properties
        if 'innodb' in self.engine:
            print("using innodb engine")
            self.dbstate.executeUpdate("create table grindertest (streamid INT,"
                                   " time INT, value DOUBLE, CONSTRAINT pk_ts"
                                   " PRIMARY KEY (streamid, time) ) ENGINE=InnoDB "
                                   " ROW_FORMAT=COMPRESSED")
        elif 'myisam' in self.engine:
            print("using myisam engine")
            self.dbstate.executeUpdate("create table grindertest (streamid INT,"
                                   " time INT, value DOUBLE, CONSTRAINT pk_ts"
                                   " PRIMARY KEY (streamid, time) )")
 
            self.dbstate.executeUpdate("ALTER TABLE grindertest ENGINE = myisam")


        #################Other things go here like clearing cache
        #clear MySQL Query Cache
        self.dbstate.executeUpdate("RESET QUERY CACHE")
        self.dbstate.executeUpdate("set global query_cache_size = 8000000")
        #finally, reset the connection/statement
        self.reset_conn_state()

    def run_insert_w(self):
        valmaker = self.insertGenerator.next() #potential StopIteration()
        overallstart = time.time()
        completiontime = 0
        for roundvals in valmaker: #for catches the Sub-StopIteration
            conn, s = self.dbconn, self.dbstate
            queryend = ''
            for tup in roundvals:
                queryend += str(tup) + ','
            queryend = queryend[:-1]
            starttime = time.time()
            s.executeUpdate("insert into grindertest values " + queryend)
            endtime = time.time()
            completiontime += (endtime - starttime)
            self.reset_conn_state()	
        return [overallstart, endtime, completiontime]


    def run_query_all(self, debug=False):
        #this needs to be paginated, otherwise the statement can't handle it
        conn, s = self.dbconn, self.dbstate
        pts_query = s.executeQuery("select count(time) as ptsindb from grindertest")
        pts_query.next()
        pts_in_db = pts_query.getInt("ptsindb") 
        ptcounter = 0
        origstarttime = time.time()
        completiontime = 0
        debugout = []
        while ptcounter < pts_in_db:
            self.reset_conn_state()
            conn, s = self.dbconn, self.dbstate
            starttime = time.time()
            temp = s.executeQuery("select * from grindertest limit " + str(ptcounter) + ", 1000")
            endtime = time.time()
            if debug:
                self.query_debugger(temp, debugout)
            completiontime += (endtime - starttime)
            ptcounter += 1000 
        if not debug:
            return [origstarttime, endtime, completiontime]
        return debugout

    def query_debugger(self, resultset, appendlist):
        while resultset.next():
            appendlist.append([resultset.getInt("streamid"), resultset.getInt("time")])
        #no return since this just appends to the list

    def query(self, records, streams, debug=False):
        """Query "records" records from "streams" streams""" 
        #might want to paginate this eventually
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
        debugout = []

        if default_starttime >= lastpossible:
            print("WARNING: timerange starts before earliest, resorting to" + 
                    " forced lastpossible")
            starttime = lastpossible
        else:  
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

        if debug:
            self.query_debugger(temp, debugout)
            return debugout


        completiontime = endtime - starttime
        return [starttime, endtime, completiontime]




    def query_single(self, records, streamid, debug=False):
        """Query last "records" records from the stream "streamid"."""
        """Works for both postgres and mysql"""
        conn, s = self.dbconn, self.dbstate
        debugout = []
 
        querystr = "select * from grindertest where streamid="
        querystr += str(streamid)
        querystr += " order by time desc limit "
        querystr += str(records)
        starttime = time.time()
        temp = s.executeQuery(querystr)
        endtime = time.time()
        if debug:
            self.query_debugger(temp, debugout)
            return debugout

        completiontime = endtime - starttime
        return [starttime, endtime, completiontime]







