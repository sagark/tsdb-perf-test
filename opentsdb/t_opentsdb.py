#Java/SQL Stuff
from java.lang import *

#misc
import time
import sys
import subprocess
import random

#this is the recommended way of working with opentsdb
import socket
import urllib2 #for graceful shutdown

#project specific
from framework import DBTest


class OpenTSDBAccess(DBTest):
    def __init__(self):
        """For reading db, these properties are defined in the 'driver'"""
        #general properties
        #N/A

        #setup driver(s)
        self.driver_simple = "readingdb_drv/reading_simple.py"
        self.driver_complex = "readingdb_drv/reading_complex.py"
    
        #start connection/statement
        self.reset_conn_state() #THIS IS REQUIRED BEFORE self.prepare()

        #prepare the database for an experiment and create conn/state
        self.prepare()

    def reset_conn_state(self):
        #does nothing for readingdb
        pass
 
    def close_all(self):
        #does nothing for readingdb
        pass


    def check_close(self, ob):
        #does nothing for readingdb
        pass

    def get_db_size(self):
        # possibly try hbase shell status 'detailed'
        dbsize = 3
        return str(dbsize) #go back to str

    def prepare(self):
        devnull = open('/dev/null', 'w')
        # prepare by deleting all data files
        # make sure readingdb_drv/prep_server has been chmod +x'd
        # first we need to find out if we are running as root:
        try:
            urllib2.urlopen('http://localhost:4242/diediedie')
            time.sleep(10) #give it 10 seconds to shut down
        except urllib2.URLError:
            pass #this is fine, there's no opentsdb running already
        a = subprocess.Popen(["opentsdb_drv/start_opentsdb"], stdout=devnull, stderr=devnull)
        time.sleep(20)
        print("opentsdb server running")
        

    def run_insert_w(self):
        #generate and store values to file
        devnull = open('/dev/null', 'w')
        roundgen = self.insertGenerator.next() #potential StopIteration()
        streamcount = roundgen.streams
        if roundgen.pt_time == 946684800:
            #if pt_time is equal to the start, we need to make the streams
            for x in range(1, streamcount+1):
                subprocess.call(['tsdb', 'mkmetric', 'stream'+str(x)], stdout = devnull, stderr = devnull)
        completiontime = 0
        overallstart = time.time()
        for vallist in roundgen:
            for valpair in vallist:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('localhost', 4242))
                starttime = time.time()
                sock.send('put stream'+str(valpair[0]) + ' ' + str(valpair[1]) 
                                + ' ' + str(valpair[2]) + ' host=localhost\n')
                endtime = time.time()
                sock.close()
                completiontime += (endtime-starttime)
       
 
        return [overallstart, endtime, completiontime]

    def run_insert_h(self):
        #mkmetric as we go
        #should be fairly well-optimized at this point
        #special height-wise insert for readingdb
        roundgen = self.insertGenerator.next() #potential StopIteration()
        

        
        return returnlist


    def run_query_all(self, debug=False):
        if debug:
            a = subprocess.Popen(["readingdb_drv/run_query_all.py", "'True'"], stdout=subprocess.PIPE)
        else:
            a = subprocess.Popen(["readingdb_drv/run_query_all.py", "'False'"], stdout=subprocess.PIPE)
        b = a.communicate()[0]
        returnlist = eval(b)

        if debug:
            debugout = file('tempfiles/debugout')
            dout = debugout.readlines()
            debugout.close()
            debugout = []
            for row in dout:
                debugout += eval(row)
            return debugout


        return returnlist
       

    def query(self, records, streams, debug=False):
        """Query "records" records from "streams" streams"""
        
        ##getting latest point in db
        a = subprocess.Popen(["readingdb_drv/reading_getlatest.py"], stdout=subprocess.PIPE)
        b = a.communicate()[0]
        last = int(eval(b))
    
        #latest = file('tempfiles/lasttime')
        #last = int(eval(latest.read()))
        #latest.close()
        #print(last)
        lastpossible = last - records + 1
        default_starttime = 946684800

        if default_starttime >= lastpossible:
            print("WARNING: timerange starts before earliest, resorting to" + 
                    " forced lastpossible")
            qstarttime = lastpossible
        else:  
            qstarttime = random.randrange(default_starttime, lastpossible)

        qendtime = qstarttime + records 
        params = [streams, qstarttime, qendtime]
        
        if debug:
            c = subprocess.Popen(["readingdb_drv/query.py", str(params), "'True'"], stdout=subprocess.PIPE)
        else:
            c = subprocess.Popen(["readingdb_drv/query.py", str(params), "'False'"], stdout=subprocess.PIPE)          
        d = c.communicate()[0]
        returnlist = eval(d)

        if debug:
            debugout = file('tempfiles/debugout')
            dout = debugout.readlines()
            debugout.close()
            debugout = []
            for row in dout:
                debugout += eval(row)
            return debugout

        
        return returnlist
