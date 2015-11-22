# Site Monitoring

> &copy; 2015 Scott Daniels <provideyourown.com>
> under GNU General Public License

The Site Monitoring library is a collection of python scripts that provide monitoring tools for servers and websites. These scripts can be:
1) Run from the command line to get the needed information
2) Individual functions in each file can be loaded and called from custom python applications to provide customizable output.

Each of these utilities require a `host` to be specified. The `host` can be either a named host in your `~/.ssh/config` file, or it can be `USER@DOMAIN/IP`. Server utilities can also be called on your local computer. In this case, use either `local` or `localhost` for the host specification.

To execute these utilities as standalone scripts, make them executable via:

    $ chmod +x FILENAME.py
    
You can also execute the standalone scripts repeatedly with a simple bash function:

    repeat() { INT=$1; shift; while true; do $*; sleep $INT; done; }

Usage (repeat systemload every 15 secs):  
    
    repeat 15 ./systemload.py local [-i 2]



## Server Utilities

###System Load

####Python Funcs

`getCpuLoad(server, interval)`

Given the host definition for the server, and an interval (in secs), return the average cpu load over that interval as a percentage.

####Standalone usage:

./systemload.py HOST [-i 5.0]

-i optionally specifies the interval. The default is 1.0 seconds.

Prints the cpu load as a percentage


###Memory Usage

####Python Funcs

`getMemoryUsage(server)`

Given the host definition for the server, return the memory *used, total* and *swap*. *Used* and *total* memory is in Megabytes, whereas *swap* is in percentage.

####Standalone usage:

./memoryusage.py HOST

Prints the memory used as a percentage of total available, the total available, and the percentage of swap memory used.





