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
        # hbase shell is way too slow - enable metrics in hbase/hadoop and tail the logfile instead
        a = subprocess.Popen(["tail", "-2", "/tmp/metrics_hbase.log"], stdout = subprocess.PIPE)
        b = a.communicate()[0].split()
        points = []
        for x in b:
            if 'memstoreSizeMB' in x or 'rootIndexSizeKB' in x or 'storefileIndexSizeMB' in x or 'totalStaticIndexSizeKB' in x:
                points.append(x.replace(',', '').split('='))
        totalsize = 0
        for x in points:
            if 'MB' in x[0]:
                totalsize += int(x[1])*1000000
            elif 'KB' in x[0]:
                totalsize += int(x[1])*1000
        dbsize = totalsize
        return str(dbsize)
        
    def prepare(self):
        devnull = open('/dev/null', 'w')
        # prepare by deleting all data files
        # make sure opentsdb_drv/prep_server has been chmod +x'd
        # first we need to find out if we are running as root:
        try:
            urllib2.urlopen('http://localhost:4242/diediedie')
            time.sleep(10) #give it 10 seconds to shut down
        except: #pretty much any reasonable error here means the tsd is not running
            pass #this is fine, there's no opentsdb running already
        a = subprocess.Popen(["opentsdb_drv/start_opentsdb"])
        time.sleep(20)
        print("opentsdb server running")
        

    def run_insert_w(self):
        #generate and store values to file
        devnull = open('/dev/null', 'w')
        roundgen = self.insertGenerator.next() #potential StopIteration()
        self.streamcount = roundgen.streams
        streamcount = self.streamcount
        if roundgen.pt_time == 946684800:
            #if pt_time is equal to the start, we need to make the streams
            origend = streamcount+1
            for x in range(1, streamcount+1, 100):
                end = x + 100
                buildup = ["stream" + str(z) for z in range(x, min(origend, end))]
                cmd = ['tsdb', 'mkmetric'] + buildup
                subprocess.call(cmd, stdout = devnull, stderr = devnull)
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



    def run_query_all(self, debug=False):
        #no 'real' query, use HTTP and urllib2
        queryurlform = 'http://localhost:4242/q?start=1343740417s-ago&m=sum:stream%s&ascii'
        overallstart = time.time()
        completiontime = 0
        for x in range(1, self.streamcount+1):
            qurl = queryurlform % x 
            starttime = time.time()
            a = urllib2.urlopen(qurl)
            endtime = time.time()
            completiontime += (endtime - starttime)
            if debug:
                c = a.readlines() 
        return [overallstart, endtime, completiontime]
       

    def query(self, records, streams, debug=False):
        """Query "records" records from "streams" streams"""
        returnlist = [1, 1, 1]
        #stuff here
        if debug:
            debugout = []
            return debugout

        return returnlist
