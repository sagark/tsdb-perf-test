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
        totalsize = 0
        props = {'tsdb': [], 'tsdb-uid': []}
        a = subprocess.Popen(["hbase", "shell", "opentsdb_drv/db_size"], stdout = subprocess.PIPE)
        b = a.communicate()
        cleanup = b[0].split()
        while 'tsdb' not in cleanup[0]:
            cleanup.pop(0)
        cleanup.pop(0)
        while 'tsdb' not in cleanup[0]:
            tmp = cleanup.pop(0)
            if 'Size' in tmp:
                props['tsdb'].append(tmp)
        cleanup.pop(0)
        for tmp in cleanup:
            if 'Size' in tmp:
                props['tsdb-uid'].append(tmp)
        #print(props['tsdb'])
        allprops = props['tsdb'] + props['tsdb-uid']
        for x in allprops:
            x = x.replace(',', '')
            x = x.split('=')
            if 'MB' in x[0]:
                totalsize += int(x[1])*1000000 #convert to bytes
            elif 'KB' in x[0]:
                totalsize += int(x[1])*1000 #convert to bytes    
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
                subprocess.call(['tsdb', 'mkmetric', 'stream'+str(x)], 
                                           stdout = devnull, stderr = devnull)
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
        returnlist = [1, 1, 1]
        #stuff here
        if debug:
            debugout = []
            return debugout

        return returnlist
       

    def query(self, records, streams, debug=False):
        """Query "records" records from "streams" streams"""
        returnlist = [1, 1, 1]
        #stuff here
        if debug:
            debugout = []
            return debugout

        return returnlist
