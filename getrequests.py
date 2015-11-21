#!/usr/bin/env python

# Author: Scott Daniels
#
# Search latest apache access.log file and count the number of recent requests
#
# Usage:
# From CLI:
#  ./getrequests.py http://example.com/
#
# From Browser:
# http://example.com/cgi-bin/getrequests.py http://example.com
#


import sys
import re
#from time import strftime
from datetime import datetime, timedelta
import cgitb

cgitb.enable()


url = sys.argv[1]


logfile = '../logs/access.' + strftime("%Y.%m.%d") + '.log'
f = open(logfile)
content = f.read()

now = datetime.now()
last_hour = now - timedelta(hours=1)
last_min = now - timedelta(minutes=1)

hrstr = last_hour.strftime("%d/%b/%Y:%H")
minstr = last_min.strftime("%d/%b/%Y:%H:%M")


req_hr = len(re.findall(hrstr + '.*GET.*HTTP.*' + url, content))
req_min = len(re.findall(minstr + '.*GET.*HTTP.*' + url, content))

print "Content-Type: text/html"
print
print "<title>Requests</title>"

print "Requests per hour: {num}<br/>".format(num=req_hr)
print "Requests per minute: {num}<br/>".format(num=req_min)

