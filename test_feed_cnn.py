#!/usr/bin/env python
# feed test
# Author: David Bradway (david.bradway@gmail.com)
#
import time
import requests

# Last results to check if the results have changed
dems_last = -1
reps_last = -1

url = 'http://data.cnn.com/ELECTION/2016/bop/p.json'
# print(url)

# Main program logic follows:
if __name__ == '__main__':
    # Parse a website to find the current totals
    try:
        r = requests.get(url)
        content = r.json()
        dems = int(content['candidates'][1]['evotes'])

        reps = int(content['candidates'][0]['evotes'])

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
