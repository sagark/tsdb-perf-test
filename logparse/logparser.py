import sys
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

#filename = sys.argv[1]

DB_NAMES = ["mysql-myisam", "mysql-innodb", "opentsdb", "postgres", 
                                                        "readingdb", "scidb"]
itervals = ['r-', 'g-', 'b-', 'k-', 'r:', 'g:', 'b:', 'k:']
graph_1_iter = iter(itervals)
graph_2_iter = iter(itervals)



def parsedata(filearg):
    log = file(filearg)
    lines = log.readlines()
    log.close()

    while "Started Logging" not in lines[0]:
        lines.pop(0)

    #get title
    title = lines.pop(0).split("Started Logging: ")[1].split(' at')[0]

    while "[ run-0 ]" not in lines[0]:
        lines.pop(0)

    #print(lines[0])

    points = []

    counter = 0
    while "finished" not in lines[0]:
        insert = lines.pop(0).split(": ")[2]
        query = lines.pop(0).split(": ")[2]
        size = lines.pop(0).split("now ")[1].replace(" bytes.", "")
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

    for name in DB_NAMES:
        if name in filearg:
            a = (name, a)
    return a

db_arrays = []
for x in sys.argv[1:]:
    db_arrays.append(parsedata(x))

fig = plt.figure(figsize=(20, 20), dpi=300)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.set_title('Add 1 Record to 10000 Streams, 100 times')
ax1.set_xlabel('# of Records in DB')
ax1.set_ylabel('Time for operation completion (s)')
ax2.set_title('Add 1 Record to 10000 Streams, 100 times')
ax2.set_xlabel('# of Records in DB')
ax2.set_ylabel('DB size (MB)')

legend1 = ()
legend2 = ()

for a in db_arrays:
    name = a[0]
    a = a[1]
    x = a[:,0]
    y1 = a[:,1]
    y2 = a[:,2]
    y3 = a[:,3]
    ax1.plot(x, y1, graph_1_iter.next(), x, y2, graph_1_iter.next())
    ax2.plot(x, y3, graph_2_iter.next())
    legend1 += ('Insertion (' + name + ')', 'Query (' + name + ')')
    legend2 += (name,)

leg = ax1.legend(legend1, 'upper left', shadow=True)
leg2 = ax2.legend(legend2, 'upper left', shadow=True)

plt.savefig('test.png')
