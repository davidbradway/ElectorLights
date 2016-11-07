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
        r = requests.get(url)
        content = r.text
        dem_start = '|US1746;Dem;'
        sub = content[content.find(dem_start)+len(dem_start):]
        dem_end = sub.find(';')
        dems = int(sub[:dem_end])

        rep_start = '|US8639;GOP;'
        sub = content[content.find(rep_start)+len(rep_start):]
        rep_end = sub.find(';')
        reps = int(sub[:rep_end])

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
