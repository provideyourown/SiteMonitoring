#!/usr/bin/env python

"""
Display the system load over an interval of secs. Can be called on a remote server or use 'local' or 'localhost' for your computer

Usage:

./systemload.py MYSERVER [-i 5.0]

The result is returned as a percentage.
"""

import argparse
from subprocess import check_output
import time

INTERVAL = 1.0


def getTimeList(server):
    """
    Fetches a list of time units the cpu has spent in various modes
    Detailed explanation at http://www.linuxhowtos.org/System/procstat.htm
    """
    if server in ['local', 'localhost']:
      cpuStats = file("/proc/stat", "r").readline()
    else:
      stats = check_output(['ssh', server, 'cat', '/proc/stat', '|', 'grep', 'cpu'])
      cpuStats = stats.split('\n', 1)[0] # get first line
    columns = cpuStats.replace("cpu", "").split(" ")
    return map(int, filter(None, columns))

def deltaTime(server, interval):
    """
    Returns the difference of the cpu statistics returned by getTimeList
    that occurred in the given time delta
    """
    timeList1 = getTimeList(server)
    time.sleep(interval)
    timeList2 = getTimeList(server)
    return [(t2-t1) for t1, t2 in zip(timeList1, timeList2)]

def getCpuLoad(server, interval):
    """
    Returns the cpu load as a value from the interval [0.0, 1.0]
    """
    dt = list(deltaTime(server, interval))
    idle_time = float(dt[3])
    total_time = sum(dt)
    load = 1-(idle_time/total_time)
    return load

if __name__ == '__main__': # allow funcs above to be imported as a module

    parser = argparse.ArgumentParser(description='Get cpu load over interval for a server/computer.')
    parser.add_argument("server", help='Enter server name as defined in ~/.ssh/config or user@ip. NB: public key should be uploaded to server. For local computer use either local or localhost')
    parser.add_argument('-i', '--interval', dest='interval', default=1.0, action='store', nargs='?', type=float, help='Enter time interval. Default = 1.0 secs')
    args = parser.parse_args()

    #print 'interval: %s' % args.interval

    print "System load: {:.2f} %".format(getCpuLoad(args.server, args.interval)*100) 
    exit()
