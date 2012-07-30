#!/usr/bin/python

import readingdb as rdb
import sys
import time

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

debug=True

starttime = time.time()
temp = rdb.db_query(list(range(1, 10001)), 0, 1000000000000)
endtime = time.time()
completiontime = endtime-starttime

if debug:
    debugout = file('tempfiles/debugout', 'w')
    debugout.write(str(temp))
    debugout.close()

rdb.db_close(a)

print([starttime, endtime, completiontime])

sys.exit()
