#!/usr/bin/env python

"""
Display the system memory usage. Can be called on a remote server or use 'local' or 'localhost' for your computer

Usage:

./memoryusage.py MYSERVER

"""

import argparse
import subprocess

def getMemoryUsage(server):
    """
    Returns the cpu load as a value from the interval [0.0, 1.0]
    """
    if server in ['local', 'localhost']:
      result = subprocess.check_output('free -m', shell=True)
    else:
      result = subprocess.check_output('ssh %s "free -m"' % server, shell=True)
    lines = result.split('\n')
    toks = lines[2].split() # split along whitespace
    used = int(toks[2])
    free = int(toks[3])
    total = used + free
    
    toks = lines[3].split()
    swap = float(toks[2]) / float(toks[1]) if int(toks[1]) else 0
    return used, total, swap


if __name__ == '__main__': # allow funcs above to be imported as a module

    parser = argparse.ArgumentParser(description='Get memory usage for a server/computer.')
    parser.add_argument("server", help='Enter server name as defined in ~/.ssh/config or user@ip. NB: public key should be uploaded to server. For local computer use either local or localhost')
    args = parser.parse_args()

    used, total, swap = getMemoryUsage(args.server)
    print "Memory usage: {:.2f}% of {}Mb (swap: {:.2f}%)".format(100.0*used/total, total, swap*100) 
    exit()
