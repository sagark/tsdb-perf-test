#!/usr/bin/python

import readingdb as rdb
import sys

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

for x in sys.argv[1:]:
    exec(x)


"""call this with:
python reading.py "rdb.db_add(a, 1, [(x, 0, x) for x in xrange(0, 100)])
" "print rdb.db_query(1, 0, 100, conn=a)"
"""

