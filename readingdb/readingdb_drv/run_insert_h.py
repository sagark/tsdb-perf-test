#!/usr/bin/python

import readingdb as rdb
import sys
from threading import Thread
import time
from framework import SubGenerator_h

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

genprops = eval(sys.argv[1])

rangesetup = genprops.pop(2)
rangesetup[1] = rangesetup[1] + 1 #fix off by one

roundgen = SubGenerator_h(genprops[0], genprops[1], range(*rangesetup), genprops[2])

completiontime = 0
overallstart = time.time()
for roundvals in roundgen:
    newvals = list(map(lambda x: (x[1], 0, x[2]), roundvals))
    streamid = roundvals[0][0]
    starttime = time.time()
    rdb.db_add(a, streamid, newvals)
    endtime = time.time()
    completiontime += (endtime - starttime)
overallfinish = time.time()
timings = [overallstart, overallfinish, completiontime]



rdb.db_close(a)

print(timings)

sys.exit()
