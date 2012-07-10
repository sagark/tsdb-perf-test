#Java/SQL Stuff
from java.lang import *
from java.sql import *

#misc
import time
import sys

#project specific
from outline import DBTest


class PostgresAccess(DBTest):
    def __init__(self):
        #general properties
        self.db = "grindertest"
        self.urlroot = "jdbc:postgresql://localhost/"
        self.dbabout = "information_schema"
        self.user = "postgres"
        self.passw = "postgres"
        self.dbconn = None
        self.dbstate = None
        self.dbaboutconn = None
        self.dbaboutstate = None

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

        #################Other things go here like clearing cache
        #clear MySQL Query Cache
        self.dbstate.executeUpdate("RESET QUERY CACHE")

        #finally, reset the connection/statement
        self.reset_conn_state()

