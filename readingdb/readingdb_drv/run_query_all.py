#!/usr/bin/python

import readingdb as rdb
import sys
import time

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

#print(sys.argv[1])
debug = eval(sys.argv[1])

starttime = time.time()
temp = rdb.db_query(list(range(1, 10001)), 0, 1000000000000)
endtime = time.time()
completiontime = endtime-starttime

if debug:
    removeempty = lambda x: x != []
    debugout = file('tempfiles/debugout', 'w')
    processed = list(temp)
    processed = list(map(list, processed))
    for x in range(len(processed)):
        processed[x] = list(map(lambda z: [x+1, int(z[0])], processed[x]))
    processed = filter(removeempty, processed)
    for line in processed:
        debugout.write(str(line) + "\n")
    debugout.close()

rdb.db_close(a)

print([starttime, endtime, completiontime])

sys.exit()
