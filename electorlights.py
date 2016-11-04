#!/usr/bin/env python
# Raspberry Pi Neopixel ElectorLights
# Author: David Bradway
# 
# Uses NeoPixel Python library wrapper by Tony DiCola (tony@tonydicola.com)
#  and NeoPixel/ rpi_ws281x library created by Jeremy Garff.

import math
import time
from bs4 import BeautifulSoup
import requests

PI = True
TESTING = False

if PI:
    import neopixel

# LED strip configuration:
LED_COUNT = 89      # CHANGEME! Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)

# Customize this once we find a site with live-updating numbers
url = 'http://www.270towin.com/'
dem_id = 'dem_ev'
rep_id = 'rep_ev'


# Define functions which animate LEDs in various ways.
def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def reset_all(strip, wait_ms=50):
    """Set all pixels to green one at a time"""
    color_wipe(strip, neopixel.Color(0, 255, 0), wait_ms)


def set_democrats(strip, electors, wait_ms=50):
    """Wipe blue in from the left side one pixel at a time."""
    # There are 538 total possible electors
    # We have LED_COUNT number of LEDs to represent them
    # So we use each LED to represent (538 / LED_COUNT) electors
    num_leds_to_change = electors // (538 // LED_COUNT)
    print("Num LEDS to change " + repr(num_leds_to_change))
    # We can represent the fractional part with the color level
    # We use modulo operator to partially light up the last LED
    remainder_level = electors % (538 // LED_COUNT)
    print("Remainder " + repr(remainder_level))
    if PI:
        for i in range(num_leds_to_change):
            # Turn these fully blue, one at a time
            strip.setPixelColor(i, neopixel.Color(0, 0, 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
        # If there is a fractional part, turn it a proportional shade
        if remainder_level > 0:
            strip.setPixelColor(num_leds_to_change,
                                neopixel.Color(0, 0, math.floor(remainder_level
                                                * 255 / (538 // LED_COUNT))))
            strip.show()
            time.sleep(wait_ms/1000.0)


def set_republicans(strip, electors, wait_ms=50):
    """Wipe red in from the right side one pixel at a time."""
    num_leds_to_change = electors // (538 // LED_COUNT)
    print("Num LEDS to change " + repr(num_leds_to_change))
    remainder_level = electors % (538 // LED_COUNT)
    print("Remainder " + repr(remainder_level))
    if PI:
        for i in range(num_leds_to_change):
            strip.setPixelColor(LED_COUNT-i, neopixel.Color(255, 0, 0))
            strip.show()
            time.sleep(wait_ms/1000.0)
        if remainder_level > 0:
            strip.setPixelColor(LED_COUNT - num_leds_to_change,
                                neopixel.Color(math.floor(remainder_level
                                        * 255 / (538 // LED_COUNT)), 0, 0))
            strip.show()
            time.sleep(wait_ms/1000.0)


# Last results to check if the results have changed
dems_last = 0
reps_last = 0


# Main program logic follows:
if __name__ == '__main__':

    if PI:
        # Create NeoPixel object with appropriate configuration.
        my_strip = neopixel.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
        # Intialize the library (must be called once before other functions).
        my_strip.begin()
        reset_all(my_strip)

    print('Press Ctrl-C to quit.')
    while True:
        # Parse a website to find the current totals
        try:
            print('Scrape')
            if TESTING:
                url = 'https://www.random.org/integers/?num=1&min=1&max=270&col=1&base=10&format=plain&rnd=new'
                r = requests.get(url)
                dems = r.text
                r = requests.get(url)
                reps = r.text
            else:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                dems = soup.find(id=dem_id).text
                reps = soup.find(id=rep_id).text

            if (dems, reps) != (dems_last, reps_last):
                # New results, do stuff
                print("Dem electors " + dems)
                set_democrats(my_strip, dems)
                print("Rep electors " + reps)
                set_republicans(my_strip, reps)
                # Save the current totals for when this runs in a loop
                (dems_last, reps_last) = (dems, reps)

        except:
            print('error')
            pass
        if TESTING:
            time.sleep(5)
        else:
            time.sleep(5*60)
