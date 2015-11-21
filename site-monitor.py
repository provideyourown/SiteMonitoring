#!/usr/bin/env python

"""
Adapted from site-up.py by David Hall - https://gist.github.com/skwashd/1225092

Provides continuous confirmation of a site's being up, along with its load time.

Given a url and a string contained in the site's page, it will check to see if the page returns this string successfully
along with the time it took to do so.

Parameters: url, testString, [test_interval]
Usage: ./site-monitor.py http:example.com 'this is an example site' [30]
"""


import sys
import time
import requests
from datetime import datetime as dt

DELAY_INT = 5.0

def getSite(url, testStr):
  start = time.time()
  try:
    r = requests.get(url)
  except:
    end = time.time()
    return False, True, end-start
  end = time.time()
  isUp = r.status_code == 200
  isCorrect = testStr in r.text
  return isUp, isCorrect, end-start

url = sys.argv[1]
searchStr = sys.argv[2]
interval = float(sys.argv[3]) if len(sys.argv) > 3 else DELAY_INT

while True:
  isUp, isCorrect, deltaT = getSite(url, searchStr)
  upStr = 'Site is UP' if isUp else 'Site is DOWN'
  validStr = '' if isCorrect or not isUp else '; Site is INCORRECT'
  timeStr = '; load time = %s secs' % round(deltaT, 2)
  timeStamp = dt.strftime(dt.now(),'%Y-%m-%d %H:%M:%S')
  print timeStamp + ' - ' + upStr + validStr + timeStr
  time.sleep(interval)
  
