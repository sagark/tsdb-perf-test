#!/usr/bin/python

import readingdb as rdb
import sys
import time
from framework import SubGenerator_w

props = eval(sys.argv[1])

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

rangestep = props.pop()
rangemax = props.pop()
rangemin = props.pop()
rebuildrange = range(rangemin, rangemax+1, rangestep)

roundgen = SubGenerator_w(*props, valid_values=rebuildrange)


completiontime = 0
overallstart = time.time()
for roundvals in roundgen: #for each list in subgen
    for val in roundvals: #for each element in the list returned by subgen.next()
        starttime = time.time()
        rdb.db_add(a, val[0], [(val[1], 0, val[2])])
        endtime = time.time()
        completiontime += endtime - starttime


rdb.db_close(a)

print([overallstart, endtime, completiontime]) #put list on stdout for t_readingdb
sys.exit()
