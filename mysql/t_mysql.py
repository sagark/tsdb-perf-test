#Java/SQL Stuff
from java.lang import *
from java.sql import *
import com.mysql.jdbc.Driver

#misc
import time
import sys

#project specific
from outline import DBTest


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
    
        #start connection/create statement
        self.reset_conn_state()

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


    def clean_for_experiment(self):
        try:
            self.dbstate.executeUpdate("drop table grindertest")
        except:
            pass
        self.dbstate.executeUpdate("create table grindertest (streamid INT,"
                                   " time INT, value DOUBLE)")
        self.reset_conn_state()
