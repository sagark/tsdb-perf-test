#!/usr/bin/python

import readingdb as rdb
import sys
import time

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

params = eval(sys.argv[1])
streams = params[0]
qstarttime = 

starttime = time.time()
rdb.db_query(list(range(1, 1+streams)), qstarttime, qendtime)
endtime = time.time()
completiontime = endtime-starttime

rdb.db_close(a)

print(str([starttime, endtime, completiontime]))

sys.exit()
