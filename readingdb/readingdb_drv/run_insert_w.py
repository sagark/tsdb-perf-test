#!/usr/bin/python

import readingdb as rdb
import sys
#from threading import Thread
import time
from framework import SubGenerator_w

print(sys.argv[1])

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

getd = file('tempfiles/tempdata')
data = getd.read()
props = eval(data)
getd.close()

roundgen = SubGenerator_w(*props)


completiontime = 0
overallstart = time.time()
for roundvals in roundgen: #for each list in subgen
    for val in roundvals: #for each element in the list returned by subgen.next()
        starttime = time.time()
        rdb.db_add(a, val[0], [(val[1], 0, val[2])])
        endtime = time.time()
        completiontime += endtime - starttime


rdb.db_close(a)

wtime = file('tempfiles/timetaken', 'w')
wtime.write(str([overallstart, endtime, completiontime]))
wtime.close()

sys.exit()
