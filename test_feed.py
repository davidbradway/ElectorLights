# feed test
# Author: David Bradway (david.bradway@gmail.com)
#
import time
from bs4 import BeautifulSoup
import requests

# Last results to check if the results have changed
dems_last = 0;
reps_last = 0;

# Customize this once we find a site with live-updating numbers
url = 'http://www.270towin.com/'
dem_id = 'dem_ev'
rep_id = 'rep_ev'

# Main program logic follows:
if __name__ == '__main__':
    # Parse a website to find the current totals
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        dems = soup.find(id=dem_id).text
        reps = soup.find(id=rep_id).text

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
