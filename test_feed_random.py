#!/usr/bin/env python
# feed test
# Author: David Bradway (david.bradway@gmail.com)
#
import time
import requests
import datetime as dt

# Last results to check if the results have changed
dems_last = -1
reps_last = -1

timestamp = dt.datetime.now()
format = "%Y%m%d%H%M%S"
s = timestamp.strftime(format)

url = 'http://s3.amazonaws.com/origin-east-elections.politico.com/mapdata/2016/US.xml?cachebuster='+s
# print(url)

# Main program logic follows:
if __name__ == '__main__':
    # Parse a website to find the current totals
    try:
        url = 'https://www.random.org/integers/?num=1&min=1&max=270&col=1&base=10&format=plain&rnd=new'
        r = requests.get(url)
        dems = r.text
        dems = int(float(dems))

        r = requests.get(url)
        reps = r.text
        reps = int(float(reps))

        if (dems,reps) != (dems_last,reps_last):
            # New results, do stuff
            print(dems)
            print(reps)
            # Save the current totals for when this runs in a loop
            (dems_last,reps_last) = (dems,reps)
    except:
        print('error')
        pass
    time.sleep(0.1)
