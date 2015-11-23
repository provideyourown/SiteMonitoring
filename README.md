# Site Monitoring

> &copy; 2015 Scott Daniels <provideyourown.com>
> under GNU General Public License

## Problem
I have often wanted/needed a way to verify a server hosting websites was up and running properly. While many fine graphical tools exist such as Munin for this purpose, I wanted a simple set of utilities that could return just the parameters I needed and how I needed them. 

I identified two different needs for metrics. The first is a cmd-line utility that I can run from my local server to test the parameter needed. The second is a set of python functions that get the same metrics that I can then call to put in a custom webpage. This webpage (a future project) would run on a local server such as a Raspberry Pi, which could then display all my metrics on a tablet display in a convenient location. A quick glance could then show that everything was running smoothly or that problems have arisen. Other possibilities include - sending an SMS message when a site goes down, and lighting up LEDs to indicate site performance, etc.

The various metrics needed can be grouped into two categories:

1. Server performance - these metrics indicate the health of the server itself. Metrics such as cpu load and memory usage are most desired.
2. Website performance - these metrics indicate the health of the webserver. Metrics include page load speed, site verification, #requests/hr, etc.

## Solution
The Site Monitoring library is a collection of python scripts that provide monitoring tools for servers and websites. These scripts can be:

1. Run from the command line to get the needed information
2. Individual functions in each file can be loaded and called from custom python applications to provide customizable output.

Each of these utilities require a `host` to be specified. The `host` can be either a named host in your `~/.ssh/config` file, or it can be `USER@DOMAIN/IP`. Server utilities can also be called on your local computer. In this case, use either `local` or `localhost` for the host specification.

To execute these utilities as standalone scripts, make them executable via:

        $ chmod +x FILENAME.py
    
You can also execute the standalone scripts repeatedly with a simple bash function (add to your ~/.bashrc or .bash_aliases file):

        repeat() { INT=$1; shift; while true; do $*; sleep $INT; done; }

Usage (repeat systemload every 15 secs):  
    
        repeat 15 ./systemload.py local [-i 2]



## Server Utilities

###System Load

This utility shows the system load as a percentage over a period of time.

####Python Funcs

        getCpuLoad(server, interval)

Given the host definition for the server, and an interval (in secs), return the average cpu load over that interval as a percentage.

####Standalone usage:

        $ ./systemload.py HOST [-i 5.0]

-i optionally specifies the interval. The default is 1.0 seconds.

Prints the cpu load as a percentage


###Memory Usage

This utility shows the memory used out of total available and the percentage of swap memory used (if any).

####Python Funcs

        getMemoryUsage(server)

Given the host definition for the server, return the memory *used, total* and *swap*. *Used* is given as a percentage, *total* memory is in Megabytes, and *swap* is in percentage.

####Standalone usage:

        $ ./memoryusage.py HOST

Prints the memory used as a percentage of total available, the total available, and the percentage of swap memory used.


## Website Utilities

###Site Test

This utility indicates if a site is up, verifies the site's page is valid, and provides the total page load time.

####Python Funcs

        getSite(url, testStr)

Tests to see if the site is up, is valid and its loading time. 

Parameters:

        url:    can be just the site's domain name or can optionally include the protocol (http/https)
        testStr:    a string within the page to verify the page loaded correctly
    
Returns:

        isUp (bool), isCorrect (bool), load-time (secs - float)
    
####Standalone usage:

        $ ./sitetest.py [http://]example.com 'this is an example site'

Prints up status, verifies integrity, and the load time.


###Get Requests

This utility counts the number of requests to a site over a period of time.

####Python Funcs

        countRequests(server,  logfile,  interval)

Counts the requests to this site over a period of minutes, with a maximum of 1440 mins (60 mins * 24 hours). 

Parameters:

        server:    host name as described above 
        logfile:   full path name for the access.log file (can be either apache or nginx standard log file)
        interval:  time interval in minutes over which to count requests
    
Returns:
    number of requests (int)
    
####Standalone usage:

        $ ./getrequests.py MYSERVER /var/www/MYSITE/logs/access.log [-i 20]

The time interval is specified by '-i' in minutes, and is optional. If not specified, the utility will return the number of requests over 3 periods of time: 10 mins, 1 hour, 24 hours (1 day)



