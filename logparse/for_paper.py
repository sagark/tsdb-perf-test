import sys
import os
import numpy as np
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter
import numpy as np
from math import sqrt


#here we go through all the dbs

DB_NAMES = ["mysql-myisam", "mysql-innodb", "opentsdb", "postgres", 
                                                        "readingdb", "scidb"]

itervals = ['k_', 'k-.', 'k--', 'k:']# ,'r:', 'g:', 'b:', 'k:']
dash_style = [[5, 5], [10, 10], [30, 30], (None, None)]
graph_1_iter = iter(itervals)
graph_2_iter = iter(itervals)
graph_3_iter = iter(itervals)
graph_1_d = iter(dash_style)
graph_2_d = iter(dash_style)
graph_3_d = iter(dash_style)




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
            
    stats = map(lambda x: list(np.array(x)), stats)
    #print(stats[0])
    #sys.exit(0)
    #now need to compute standard errors means, tack them on as the last column
    for i in range(1, len(stats)):
        statset = stats[i]
        for x in range(len(statset)):
            #print(statset[x])
            #print(type(statset[x]))
            mean = np.mean(statset[x])
            #print(mean)
            se = np.std(statset[x])/sqrt(len(statset[x]))
            statset[x] = np.append(statset[x], mean)
            statset[x] = np.append(statset[x], se)
            #print(statset[x])
    stats = map(lambda x: np.array(x), stats)
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
    skip_count = 0
    for x in points:
        if skip_count % 30 == 0:
            addtog = []
            addtog.append(x[0]) #number of points in db already
            addtog.append(10000.0/x[1][2]) #time to insert
            addtog.append(10000.0/x[2][2]) #time to query all
            addtog.append(x[3]/1000000) #db size after completion, convert to MB
            graphthis.append(addtog)
        skip_count += 1
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


fontsize = 28.0
matplotlib.rc('xtick', labelsize=fontsize)
matplotlib.rc('ytick', labelsize=fontsize)
matplotlib.rc('axes', labelsize=fontsize)
matplotlib.rc('legend', fontsize=fontsize)
matplotlib.rc('text', usetex=False)

#print(db_arrays)
fig = plt.figure(figsize=(20, 10), dpi=300)
#fig.suptitle('Adding 1 Record to 10000 Streams, 1000 Times - Averaged over 5 Runs - 8MB Cache', fontsize=18)
ax1 = fig.add_subplot(111)
#ax2 = fig.add_subplot(111)
#ax3 = fig.add_subplot(111)

#ax1.set_title('Insert (10,000 record batches, 100 records/insert)')
ax1.set_xlabel('# of Records in DB')
ax1.set_ylabel('Inserts/s')
ax1.xaxis.major.formatter.set_powerlimits((-100, 100))
"""
#ax2.set_title('Query 100 Records from 1000 Streams')
ax2.set_xlabel('# of Records in DB')
ax2.set_ylabel('Queries/s')
ax2.set_ylim(bottom=0, top=200000)
ax2.xaxis.major.formatter.set_powerlimits((-100, 100)) #stop writing as exp

#ax3.set_title('DB Size')
ax3.set_xlabel('# of Records in DB')
ax3.set_ylabel('DB size (MB)')
ax3.set_ylim(bottom=0, top=1000)
ax3.xaxis.major.formatter.set_powerlimits((-100, 100)) #stop writing as exp
"""
legend1 = ()
legend2 = ()
legend3 = ()


def my_formatter(x, pos):
    """Format 1 as 1, 0 as 0, and all values whose absolute values is between
    0 and 1 without the leading "0." (e.g., 0.7 is formatted as .7 and -0.4 is
    formatted as -.4)."""
    if x == 0:
        return ""
    else:
        return "{:,.0f}".format(x)


def my_formatter_w_zero(x, pos):
    """Format 1 as 1, 0 as 0, and all values whose absolute values is between
    0 and 1 without the leading "0." (e.g., 0.7 is formatted as .7 and -0.4 is
    formatted as -.4)."""
    return "{:,.0f}".format(x)



major_formatter = FuncFormatter(my_formatter)
major_formatter_w_zero = FuncFormatter(my_formatter_w_zero)
ax1.xaxis.set_major_formatter(major_formatter)
ax1.yaxis.set_major_formatter(major_formatter_w_zero)


for a in db_arrays:
    name = a[0]
    print("graphing: " + name)
    a = a[1]
    x = a[0][:,0]
    y1_mean = a[1][:,-2]
    y1_serr = a[1][:,-1]
    y2_mean = a[2][:,-2]
    y2_serr = a[2][:,-1]
    y3_mean = a[3][:,-2]
    y3_serr = a[3][:,-1]
#    ax1.plot(x, y1, graph_1_iter.next())
    ax1.errorbar(x, y1_mean, yerr=y1_serr, fmt=graph_1_iter.next(), dashes=graph_1_d.next())
    #ax2.plot(x, y2_mean, graph_2_iter.next())
#    ax2.errorbar(x, y2_mean, yerr=y2_serr, fmt=graph_2_iter.next(), dashes=graph_2_d.next())
    #ax3.plot(x, y3_mean, graph_3_iter.next())
#    ax3.errorbar(x, y3_mean, yerr=y3_serr, fmt=graph_3_iter.next(), dashes=graph_3_d.next())
    legend1 += (name,)
    legend2 += (name,)
    legend3 += (name,)

leg1 = ax1.legend(legend1, 'upper right', shadow=True)
#leg2 = ax2.legend(legend2, 'upper right', shadow=True)
#leg3 = ax3.legend(legend3, 'upper left', shadow=True)
#align_yaxis(x, 0, y1_mean, 0)
plt.savefig('test.pdf')
