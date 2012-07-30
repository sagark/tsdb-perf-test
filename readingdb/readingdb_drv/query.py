#!/usr/bin/python

import readingdb as rdb
import sys
import time

rdb.db_setup('localhost', 4242)
a = rdb.db_open('localhost')

debug = eval(sys.argv[2])

params = eval(sys.argv[1])
streams = params[0]
qstarttime = params[1]
qendtime = params[2]

starttime = time.time()
temp = rdb.db_query(list(range(1, 1+streams)), qstarttime, qendtime)
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
