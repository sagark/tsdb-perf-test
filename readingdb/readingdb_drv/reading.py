#!/usr/bin/python

import readingdb as rdb
import sys
from threading import Thread
import time

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

getd = file('tempdata')
data = getd.read()
roundvals = eval(data)
getd.close()

getc = file('tempcode')
code = getc.read()
getc.close()

starttime = time.time()
exec(code)
endtime = time.time()
completiontime = endtime-starttime

rdb.db_close(a)

wtime = file('timetaken', 'w')
wtime.write(str([starttime, endtime, completiontime]))
wtime.close()

sys.exit()
