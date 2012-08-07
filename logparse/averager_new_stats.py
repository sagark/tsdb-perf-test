import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from math import sqrt

#here we go through all the dbs

DB_NAMES = ["mysql-myisam", "mysql-innodb", "opentsdb", "postgres", 
                                                        "readingdb", "scidb"]

itervals = ['r-', 'g-', 'b-', 'k-', 'r:', 'g:', 'b:', 'k:']
graph_1_iter = iter(itervals)
graph_2_iter = iter(itervals)
graph_3_iter = iter(itervals)



rootdir = sys.argv[1] #with or without trailing slash
rootdir += "/" if rootdir[-1] not in "/" else "" #fix slash

rootdir += "logs/"

dbfolders = os.listdir(rootdir) #folders with the logs

#print(dbfolders)


def average_from_files(filedatalst):
    #filedatalst is a list of logs for one db
    #here, we detect if lines contain numbers and if so average them
    filedata = []
    for f in filedatalst:
        log = file(f)
        lines = log.readlines()
        filedata.append(lines)
        log.close()
    #now we have a list where each element is the contents of one log

    parsed = []
    numdiv = 0
    #cleanup the lines
    for lineset in filedata:
        parsed.append(parsedata(lineset))
        numdiv += 1
        #print(numdiv)
    #now instead of having [run1, run2, run3, etc..], arrange as 
    #[stat1, stat2, stat3] with runs inside 
    #print(parsed)
    stats = []
    
    x = parsed[0]
    #stats.append(x[:,0]) #get the first column (number of records in db), which is always aligned
    for colnum in range(0, np.shape(x)[1]):
        #print(colnum)
        stats.append(x[:,colnum]) #start the array for each stat
    for run_stats in range(1, len(parsed)):
        #print(parsed[run_stats])
        for colnum in range(1, np.shape(parsed[run_stats])[1]):
            #print(colnum)
            stats[colnum] = np.vstack((stats[colnum], parsed[run_stats][:,colnum]))
    for ar_num in range(len(stats)):
        #here, go arr > matrix then transpose
        stats[ar_num] = np.transpose(np.matrix(stats[ar_num]))
            
    #print(stats)
    stats = map(lambda x: np.array(x), stats)
    #print(stats)
    #now need to compute standard errors means, tack them on as the last column
    for x in range(len(stats[1])):
        print(stats[1][x])
        mean = np.mean(stats[1][x])
        print(mean)
        se = np.std(stats[1][x])/sqrt(len(stats[1][x]))
        stats[1][x] = np.append(stats[1][x], mean)
        stats[1][x] = np.append(stats[1][x], se)

    print(stats)


    sys.exit(0)
    #averagearr = totalarr/numdiv
    return stats


def parsedata(lines):
    """Convert data in logfile to python-readable format"""

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
        try:
            line = lines.pop(0)
            size = line.split("now ")[1].replace(" bytes.", "")
        except:
            print(line)
            print("exception parsing file")
            sys.exit(0)
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
    return a

db_arrays = []
for db in dbfolders:
    print(db)
    dbdir = rootdir + db
    lognames = os.listdir(dbdir)
    #now we have a list containing filenames for all the logs, so concatenate
    #the full filename for each and then put the list into average_from_files
    for x in range(len(lognames)):
        lognames[x] = dbdir + "/" + lognames[x]
    averagedfile = average_from_files(lognames)
    print(db)
    db_arrays.append((db, averagedfile))


print(db_arrays)

fig = plt.figure(figsize=(20, 30), dpi=300)
fig.suptitle('Adding 1 Record to 10000 Streams, 1000 Times - Averaged over 5 Runs', fontsize=18)
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

ax1.set_title('Insert (10,000 record batches, 100 records/insert)')
ax1.set_xlabel('# of Records in DB')
ax1.set_ylabel('Time for operation completion (s)')
#ax1.set_ylim(bottom = 0, top = 0.3)

ax2.set_title('Query (All records)')
ax2.set_xlabel('# of Records in DB')
ax2.set_ylabel('Time for operation completion (s)')
#ax2.set_ylim(bottom = 0, top = 1.5)

ax3.set_title('DB Size')
ax3.set_xlabel('# of Records in DB')
ax3.set_ylabel('DB size (MB)')

legend1 = ()
legend2 = ()
legend3 = ()

for a in db_arrays:
    name = a[0]
    a = a[1]
    x = a[:,0]
    y1 = a[:,1]
    y2 = a[:,2]
    y3 = a[:,3]
    ax1.plot(x, y1, graph_1_iter.next())
    ax2.plot(x, y2, graph_2_iter.next())
    ax3.plot(x, y3, graph_3_iter.next())
    legend1 += (name,)
    legend2 += (name,)
    legend3 += (name,)

leg1 = ax1.legend(legend1, 'upper left', shadow=True)
leg2 = ax2.legend(legend2, 'upper left', shadow=True)
leg3 = ax3.legend(legend3, 'upper left', shadow=True)

plt.savefig('test.png')
