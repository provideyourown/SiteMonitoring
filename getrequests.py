#!/usr/bin/env python

"""
Count the number of requests to an apache/nginx hosted site. 
An interval can be specified for the count in minutes. 
If an interval is not specified, then 3 default counts will be returned for 10 mins, 1 hr, 1 day

Usage:

./getrequests.py MYSERVER /var/www/MYSITE/logs/access.log [-i 20]

"""

import argparse
from subprocess import check_output
from datetime import datetime, timedelta
#import cgitb
#cgitb.enable()


def countRequests(server,  logfile,  interval):
    ssh = [] if server in ['local', 'localhost'] else ['ssh', server] # prefix the cmd with ssh to server if not localhost
    
    # 1st count all the lines for the date of the start time onward
    now = datetime.now()
    startT = now - timedelta(minutes=interval)
    date = startT.strftime("%d/%b/%Y")
    ts = startT.strftime("[%d/%b/%Y:%H:%M:%S")
    awkCmd = "awk -vDate=%s '{ if ($4 > Date) print }'" % ts
    cmd = ssh + ['grep "\[%s"' % date, logfile,  '|',  awkCmd, '|', 'wc -l']
    #print 'cmd: ' + ' '.join(cmd)
    cnt = int(check_output(cmd))

    # now check to see if the start time is not the current date. If it is not, then count all the lines
    # for the current date as well, and add them to the previous date count.
    nowDate = now.strftime("%d/%b/%Y")
    if nowDate != date:
        cmd = ssh + ['grep "\[%s"' % nowDate, logfile, '|', 'wc -l']
        #print 'cmd: ' + ' '.join(cmd)
        cnt += int(check_output(cmd))
        
    return cnt
    
'''
def getRequestCounts(server, logfile):
    def getLogCount(timestamp):
        if server in ['local', 'localhost']:
            content = check_output(['grep', timestamp, logfile,  '|',  'awk "{print $4}" | cut -d: -f1 | uniq -c'])
        else:
            content = check_output(['ssh', server, 'grep', timestamp, logfile,  '|',  'awk "{print $4}" | cut -d: -f1 | uniq -c'])
        return content.split()[0]
        
    # we can't use cat, because the log file is usually to large. So we'll grep the current and previous hour
    now = datetime.now()
    numHr = getLogCount(now.strftime("%d/%b/%Y:%H"))
    numDay = getLogCount(now.strftime("%d/%b/%Y"))
        
    return numHr,  numDay
'''


if __name__ == '__main__': # allow funcs above to be imported as a module

    parser = argparse.ArgumentParser(description='Count the number of requests to an apache/nginx hosted site. An interval can be specified for the count in minutes. If not specified, then 3 default counts will be returned.')
    parser.add_argument("server", help='Enter server name as defined in ~/.ssh/config or user@ip. NB: public key should be uploaded to server. For local computer use either local or localhost')
    parser.add_argument("logfile", help='Enter full pathname for the acces.log file, e.g. /var/www/mysite/logs/access.log')
    parser.add_argument('-i', '--interval', dest='interval', action='store', nargs='?', type=int, help='Enter time interval to count over in minutes. The maximum interval is 1440 (24hrs * 60mins)')
    args = parser.parse_args()
        
    if args.interval:
        num = countRequests(args.server,  args.logfile,  args.interval)
        print "Requests in last {min} minutes: {cnt}".format(min=args.interval,  cnt=num)
    else:
        numMin = countRequests(args.server,  args.logfile,  10)
        numHr = countRequests(args.server,  args.logfile,  60)
        numDay = countRequests(args.server,  args.logfile,  1440)
        print "Requests in last 10min: {}, hr: {}, day: {}".format(numMin,  numHr,  numDay)

    exit()
