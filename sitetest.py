#!/usr/bin/env python

"""
Adapted from site-up.py by David Hall - https://gist.github.com/skwashd/1225092

Provides continuous confirmation of a site's being up, along with its load time.

Given a url and a string contained in the site's page, it will check to see if the page returns this string successfully
along with the time it took to do so.

Parameters: url, testString
Usage: ./sitetest.py [http://]example.com 'this is an example site'
"""

import argparse
import time
import requests
from datetime import datetime as dt
from urlparse import urlparse

DELAY_INT = 5.0

def getSite(url, testStr):
    #print 'Checking url ({}) for {}'.format(url,  testStr)
    # check for protocol, and add it if missing
    res = urlparse(url)
    if not res.scheme: # add the protocol
        url = 'http://' + url
    start = time.time()
    try:
        r = requests.get(url)
    except:
        end = time.time()
        #print 'Got exception. Check your url.'
        return False, True, end-start
    end = time.time()
    isUp = r.status_code == 200
    #print r.status_code
    isCorrect = testStr in r.text
    return isUp, isCorrect, end-start

if __name__ == '__main__': # allow funcs above to be imported as a module
    
    parser = argparse.ArgumentParser(description='Check url for validity and load time.')
    parser.add_argument("url", help='Enter url. You can specify a domain name with or without protocol. "Http" is the default protocol.')
    parser.add_argument("test_string", help='Enter the text to search for and match on the page.')
    args = parser.parse_args()

    isUp, isCorrect, loadTime = getSite(args.url, args.test_string)
    upStr = 'Site is UP' if isUp else 'Site is DOWN'
    validStr = '' if isCorrect or not isUp else '; Site is INCORRECT'
    timeStr = '; load time = %s secs' % round(loadTime, 2)
    timeStamp = dt.strftime(dt.now(),'%Y-%m-%d %H:%M:%S')
    print timeStamp + ' - ' + upStr + validStr + timeStr
    exit()
  
