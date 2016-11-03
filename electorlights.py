#!/usr/bin/env python
# Raspberry Pi Neopixel ElectorLights
# Author: David Bradway
# 
# Uses NeoPixel Python library wrapper by Tony DiCola (tony@tonydicola.com)
#  and NeoPixel/ rpi_ws281x library created by Jeremy Garff.

import time
from bs4 import BeautifulSoup
import requests

PI = False

if (PI):
    from neopixel import *

# LED strip configuration:
LED_COUNT   = 89      # CHANGEME! Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

# Last results to check if the results have changed
dems_last = 0;
reps_last = 0;

# Customize this once we find a site with live-updating numbers
url = 'http://www.270towin.com/'
dem_id = 'dem_ev'
rep_id = 'rep_ev'


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


# Main program logic follows:
if __name__ == '__main__':

    if (PI):
        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
        # Intialize the library (must be called once before other functions).
        strip.begin()

    print('Press Ctrl-C to quit.')
    while True:
        # Parse a website to find the current totals
        try:
            print('Scrape')
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
        time.sleep(5*60)
