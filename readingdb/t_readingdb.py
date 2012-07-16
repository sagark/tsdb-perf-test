#Java/SQL Stuff
from java.lang import *

#misc
import time
import sys
import subprocess
import glob
import shlex

#project specific
from framework import DBTest


class ReadingDBAccess(DBTest):
    def __init__(self):
        """For reading db, these properties are defined in the 'driver'"""
        #general properties
        #self.db = "grindertest"
        #self.urlroot = "jdbc:mysql://localhost/"
        #self.dbabout = "information_schema"
        #self.user = "root"
        #self.passw = "toor"
        #self.dbconn = None
        #self.dbstate = None
        #self.dbaboutconn = None
        #self.dbaboutstate = None

        #setup driver
        self.driver = "readingdb_drv/reading.py"
    

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
        #######################Need to figure out what goes here.
        f = file('tempfiles/dbsize', 'w')
        
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

        a = subprocess.call(command, stdout=f)
        f.close()
        f = file('tempfiles/dbsize')
        #f = file('dbsize')
        a = f.readlines()
        a = a[-1]
        f.close()

        a = a.split('\t')[0]
        a = int(a)*1000
        return str(a)

    def prepare(self):
        #prepare by deleting all data files
        #subprocess.call(['gksudo', 'rm', '-r', '/var/lib/readingdb'])
        #subprocess.call(['gksudo', 'mkdir', '/var/lib/readingdb'])
        #subprocess.call(['gksudo', 'chown', '-R', 'readingdb',
        #                                                  '/var/lib/readingdb'])
        #make sure readingdb_drv/prep_server has been chmod +x'd
        subprocess.call(['gksudo', 'readingdb_drv/prep_server'])
        subprocess.Popen(['gksudo', 'reading-server'], stdin = None,
                                            stdout = None, stderr = None)
        time.sleep(5) #give reading-server 5 seconds to startup

    def run_insert_w(self):
        #generate and store values to file
        roundvals = self.insertGenerator.next() #potential StopIteration()
        tempfile = file('tempfiles/tempdata', 'w')
        tempfile.write(str(roundvals))
        tempfile.close()

        #generate and store code to file, ANY CODE HERE WILL BE INCLUDED IN THE
        #TIME MEASUREMENT!
        codefile = file('tempfiles/tempcode', 'w')
        execcode = """
for val in roundvals:
    rdb.db_add(a, val[0], [(val[1], 0, val[2])])
        """
        codefile.write(execcode)
        codefile.close()

        #call the "driver"
        a = subprocess.call([self.driver])

        #get the time taken list from file
        timetaken = file('tempfiles/timetaken')
        returnlist = eval(timetaken.read())
        timetaken.close()
        return returnlist

    def run_insert_h(self):
        #special height-wise insert for readingdb
        roundvals = self.insertGenerator.next() #potential StopIteration()
        #now process roundvals into groups of 100 for readingdb add
        newvals = []
        for x in range(0, len(roundvals), 100):
            if (x+100)>(len(roundvals)-1):
                newvals += [list(map(lambda x: (x[1], 0, x[2]), roundvals[x:]))]
            else:
                newvals += [list(map(lambda x: (x[1], 0, x[2]),
                                                        roundvals[x:x+100]))] 
        roundvals = [roundvals[0][0]] + newvals





        tempfile = file('tempfiles/tempdata', 'w')
        tempfile.write(str(roundvals))
        tempfile.close()

        #generate and store code to file, ANY CODE HERE WILL BE INCLUDED IN THE
        #TIME MEASUREMENT!
        codefile = file('tempfiles/tempcode', 'w')
        execcode = """
streamid = roundvals.pop(0)
for val in roundvals:
    rdb.db_add(a, streamid, val)
        """
        codefile.write(execcode)
        codefile.close()

        #call the "driver"
        a = subprocess.call([self.driver])

        #get the time taken list from file
        timetaken = file('tempfiles/timetaken')
        returnlist = eval(timetaken.read())
        timetaken.close()
        return returnlist


        assert False, "NEED TO IMPLEMENT THIS" 

    def run_query_all(self):
        codefile = file('tempfiles/tempcode', 'w')
        execcode = """
rdb.db_query(list(range(1, 10001)), 0, 1000000000000)
        """
        codefile.write(execcode)
        codefile.close()

        a = subprocess.call([self.driver])
        
        timetaken = file('tempfiles/timetaken')
        returnlist = eval(timetaken.read())
        timetaken.close()

        return returnlist
        
