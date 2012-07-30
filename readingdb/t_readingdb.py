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
        # for some reason glob and regex don't work in grinder, though they do
        # in jython, just hardcode it
        #cmd = """du -c /var/lib/readingdb/__* /var/lib/readingdb/read*"""
        #arg = shlex.split(cmd)
        #command = arg[:-2] + glob.glob(arg[-2]) + glob.glob(arg[-1])
        command = ['du', '-c', '/var/lib/readingdb/__db.005', 
        '/var/lib/readingdb/__db.002', '/var/lib/readingdb/__db.003', 
        '/var/lib/readingdb/__db.006', '/var/lib/readingdb/__db.001', 
        '/var/lib/readingdb/__db.004', '/var/lib/readingdb/readings-2.db', 
        '/var/lib/readingdb/readings-7.db', '/var/lib/readingdb/readings-4.db', 
        '/var/lib/readingdb/readings-5.db', '/var/lib/readingdb/readings-9.db', 
        '/var/lib/readingdb/readings-3.db', '/var/lib/readingdb/readings-1.db', 
        '/var/lib/readingdb/readings-0.db', '/var/lib/readingdb/readings-6.db', 
        '/var/lib/readingdb/readings-8.db']

        a = subprocess.Popen(command, stdout=subprocess.PIPE)
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
            subprocess.Popen(['reading-server'], stdin = None,
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


    def run_query_all(self):
        a = subprocess.Popen(["readingdb_drv/run_query_all.py"], stdout=subprocess.PIPE)
        b = a.communicate()[0]
        returnlist = eval(b)

        return returnlist
       

    def query(self, records, streams):
        """Query "records" records from "streams" streams"""
        
        ##getting latest point in db
        subprocess.call(["readingdb_drv/reading_getlatest.py"])
    
        latest = file('tempfiles/lasttime')
        last = int(eval(latest.read()))
        latest.close()
        print(last)
        lastpossible = last - records + 1
        default_starttime = 946684800

        if default_starttime >= lastpossible:
            print("WARNING: timerange starts before earliest, resorting to" + 
                    " forced lastpossible")
            starttime = lastpossible
        else:  
            starttime = random.randrange(default_starttime, lastpossible)

        endtime = starttime + records - 1
      


        codefile = file('tempfiles/tempcode', 'w')
        execcode = """
rdb.db_query(list(range(1, """ + str(1+streams) + """)), """ + str(starttime) + """, """ + str(endtime) + """)
"""
        codefile.write(execcode)
        codefile.close()

        a = subprocess.call([self.driver_simple])

        timetaken = file('tempfiles/timetaken')
        returnlist = eval(timetaken.read())
        timetaken.close()
        
        return returnlist
