#!/usr/bin/python

import readingdb as rdb
import sys
import time

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

debug = eval(sys.argv[2])
params = eval(sys.argv[1])
stream = params[0]
numrecs = params[1]

#get latest time
b = rdb.db_prev(stream, 100000000000, conn=a)
lasttime = int(b[0][0][0])
#print(lasttime)

starttime = time.time()
temp = rdb.db_prev(stream, lasttime, numrecs, conn=a)
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

print(str([starttime, endtime, completiontime]))

sys.exit()
