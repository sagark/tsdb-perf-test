import sys
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

filename = sys.argv[1]

log = file(filename)
lines = log.readlines()

while "Started Logging" not in lines[0]:
    lines.pop(0)

#get title
title = lines.pop(0).split("Started Logging: ")[1].split(' at')[0]

while "[ run-0 ]" not in lines[0]:
    lines.pop(0)

print(lines[0])

points = []

counter = 0
while "finished" not in lines[0]:
    insert = lines.pop(0).split(": ")[2]
    query = lines.pop(0).split(": ")[2]
    size = lines.pop(0).split("now ")[1].replace(" bytes.", "")
    #print(insert)
    #print(query)
    #print(size)
    points.append([counter, eval(insert), eval(query), eval(size)])
    counter += 10000 #number of records before each round

graphthis = []
for x in points:
    addtog = []
    addtog.append(x[0]) #number of points in db already
    addtog.append(x[1][2]) #time to insert
    addtog.append(x[2][2]) #time to query all
    addtog.append(x[3]/1000000) #db size after completion, convert to MB
    graphthis.append(addtog)

a = np.array(graphthis)
print(a)
print(a[:,0])

x = a[:,0]
y1 = a[:,1]
y2 = a[:,2]
y3 = a[:,3]

fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.plot(x, y1, 'g-', x, y2, 'r-')
ax1.set_xlabel('# of Records in DB')
ax1.set_ylabel('Time for operation completion (s)')

ax2 = ax1.twinx()
ax2.plot(x, y3, 'b-')
ax2.set_ylabel('DB size (MB)')

leg = ax1.legend(('Insertion', 'Query'),
           'upper center', shadow=True)
leg2 = ax2.legend(('DB Size',), 'upper left', shadow=True)

plt.savefig('test.png')
