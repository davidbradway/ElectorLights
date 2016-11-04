# feed test
# Author: David Bradway (david.bradway@gmail.com)
#
import time
from bs4 import BeautifulSoup
import requests

# Last results to check if the results have changed
dems_last = -1
reps_last = -1

url = 'http://www.politico.com/2016-election/results/map/president'

# Main program logic follows:
if __name__ == '__main__':
    # Parse a website to find the current totals
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.prettify())
        dems = [e.contents[0] for e in
                soup.select(".type-democrat > .stats-content > .stats-secondary > .macro")]
        reps = [e.contents[0] for e in
                soup.select(".type-republican > .stats-content > .stats-secondary > .macro")]
        dems = dems[0]
        reps = reps[0]
        if dems == '-':
            dems = 0
        if reps == '-':
            reps = 0

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
