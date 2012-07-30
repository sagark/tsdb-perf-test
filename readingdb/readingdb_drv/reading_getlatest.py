#!/usr/bin/python

import readingdb as rdb
import sys
import time

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

b = rdb.db_prev(1, 100000000000, conn=a)
lasttime = b[0][0][0]

rdb.db_close(a)

print(lasttime)

#ltime = file('tempfiles/lasttime', 'w')
#ltime.write(str(lasttime))
#ltime.close()

sys.exit()
