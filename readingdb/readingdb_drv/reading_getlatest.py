#!/usr/bin/python

import readingdb as rdb
import sys
from threading import Thread
import time

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

b = rdb.db_prev(1, 100000000000, conn=a)
lasttime = b[0][0][0]

rdb.db_close(a)

ltime = file('tempfiles/lasttime', 'w')
ltime.write(str(lasttime))
ltime.close()

sys.exit()
