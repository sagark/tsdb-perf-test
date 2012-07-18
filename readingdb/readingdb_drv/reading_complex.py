#!/usr/bin/python

import readingdb as rdb
import sys
from threading import Thread
import time
import pickle

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

#getpickle = open('tempfiles/tempgen', 'rb')
#roundgen = pickle.load(getpickle)
#getpickle.close()

getc = file('tempfiles/tempcode')
code = getc.read()
getc.close()

#starttime = time.time()
exec(code)
#endtime = time.time()
#completiontime = endtime-starttime

rdb.db_close(a)

wtime = file('tempfiles/timetaken', 'w')
###timings is a list that should be created in exec(code)
wtime.write(str(timings))
wtime.close()

sys.exit()
