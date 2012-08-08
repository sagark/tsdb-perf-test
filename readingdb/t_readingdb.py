#Java/SQL Stuff
from java.lang import *

#misc
import time
import sys
import subprocess
import random

#project specific
from framework import DBTest


class ReadingDBAccess(DBTest):
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
        d = subprocess.Popen(['ls', '/data/readingdb/'], stdout = subprocess.PIPE)
        q = d.communicate()[0]
        checks = []
        q = q.split('\n')
        for x in q:
            if 'log' not in x and x != '':
                checks.append('/data/readingdb/' + x)

        command = ['du', '-cb'] + checks

        a = subprocess.Popen(command, stdout = subprocess.PIPE)
        procout = a.communicate()
        dbsize = int(procout[0].split()[-2]) #ensure that it's an int without formatting junk
        return str(dbsize) #go back to str

    def prepare(self):
        # prepare by deleting all data files
        # make sure readingdb_drv/prep_server has been chmod +x'd
        # first we need to find out if we are running as root:
        p = subprocess.Popen(['whoami'], stdout = subprocess.PIPE)
        out, err = p.communicate()
        if 'root' in out:
            subprocess.call(['readingdb_drv/prep_server_root'])
            subprocess.Popen(['reading-server', '-d', '/data/readingdb'], stdin = None,
                                            stdout = None, stderr = None)
            # time.sleep(5) #give reading-server 5 seconds to startup
        else:
            subprocess.call(['gksudo', 'readingdb_drv/prep_server'])
            subprocess.Popen(['gksudo', 'reading-server'], stdin = None,
                                            stdout = None, stderr = None)
            time.sleep(5) #give reading-server 5 seconds to startup

    def run_insert_w(self):
        #generate and store values to file
        roundgen = self.insertGenerator.next() #potential StopIteration()
        rangemin = roundgen.valid_values[0]
        rangemax = roundgen.valid_values[-1]
        rangestep = roundgen.valid_values[1] - rangemin
        genprops = [roundgen.streams, roundgen.pt_time, rangemin, rangemax, rangestep]

        a = subprocess.Popen(["readingdb_drv/run_insert_w.py", str(genprops)], 
                                                        stdout=subprocess.PIPE)
        b = a.communicate()
        returnlist = eval(b[0])
        
        return returnlist

    def run_insert_h(self):
        #should be fairly well-optimized at this point
        #special height-wise insert for readingdb
        roundgen = self.insertGenerator.next() #potential StopIteration()
        rangemin = roundgen.valid_values[0]
        rangemax = roundgen.valid_values[-1]
        rangestep = roundgen.valid_values[1] - rangemin
        rangebuild = [rangemin, rangemax, rangestep]
        genprops = [roundgen.points, roundgen.stream, rangebuild,
                                                        roundgen.cur_pointtime]

        #call the "driver"
        a = subprocess.Popen(["readingdb_drv/run_insert_h.py", str(genprops)], 
                                                        stdout=subprocess.PIPE)
        b = a.communicate() #also eliminates race condition from Popen
        returnlist = eval(b[0])
        
        return returnlist


    def run_query_all(self, debug=False):
        if debug:
            a = subprocess.Popen(["readingdb_drv/run_query_all.py", "'True'"], stdout=subprocess.PIPE)
        else:
            a = subprocess.Popen(["readingdb_drv/run_query_all.py", "'False'"], stdout=subprocess.PIPE )
        b = a.communicate()
	b = b[0]
	if c is not None:
		print(c)
		sys.exit(0)
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
            c = subprocess.Popen(["readingdb_drv/query.py", str(params), "'False'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)         
        d = c.communicate()
        q = d[1]
        d = d[0]

        if q not in (None, ''):
            print(q)
            raise Exception(str(q))



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

    def query_single(self, records, streamid, debug=False):
        params = [streamid, records]
        if debug:
            c = subprocess.Popen(["readingdb_drv/query_single.py", str(params), "'True'"], stdout=subprocess.PIPE)
        else:
            c = subprocess.Popen(["readingdb_drv/query_single.py", str(params), "'False'"], stdout=subprocess.PIPE)
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
