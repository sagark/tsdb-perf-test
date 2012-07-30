#Java/SQL Stuff
from java.lang import *
from java.sql import *

#misc
import time
import sys
import random

#project specific
from framework import DBTest
from dbconfig import DBconfig


class PostgresAccess(DBTest):
    def __init__(self):
        #general properties
        self.db = DBconfig.db
        port = DBconfig.port
        self.urlroot = "jdbc:postgresql://localhost:" + port + "/"
        self.dbabout = DBconfig.dbabout
        self.user = DBconfig.user
        self.passw = DBconfig.passw
        self.dbconn = None
        self.dbstate = None
        self.dbaboutconn = None #not needed for postgres
        self.dbaboutstate = None #not needed for postgres

        #setup driver
        self.driver = "org.postgresql.Driver"
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
        
    def close_all(self):
        self.check_close(self.dbstate)
        self.check_close(self.dbconn)

    def check_close(self, ob):
        try:
            ob.close()
        except:
            pass


    def get_db_size(self):
        size = self.dbstate.executeQuery("SELECT pg_database_size"
                                              "('grindertest')")
        size.next()
        size = size.getString("pg_database_size")
        return size

    def prepare(self):
        # reset the table, create if it doesn't exist
        try:
            self.dbstate.executeUpdate("drop table grindertest")
        except:
            pass
        self.dbstate.executeUpdate("create table grindertest (streamid INT,"
                                   " time INT, value DOUBLE PRECISION, "
                                   "CONSTRAINT pk_ts PRIMARY KEY (streamid, "
                                    "time) )")
        #the end of this query creates the primary key and automatically creates 
        #an index in mysql

        #################Other things go here like clearing cache
        #To clear Postgres Cache, you have to restart the database, there is no
        #command to do it automatically

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
            temp = s.executeQuery("select * from grindertest limit 1000 offset " + str(ptcounter))
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


