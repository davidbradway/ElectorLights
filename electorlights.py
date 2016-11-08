#!/usr/bin/env python
# Raspberry Pi NeoPixel ElectorLights
# Author: David Bradway
# 
# Uses NeoPixel Python library wrapper by Tony DiCola (tony@tonydicola.com)
#  and NeoPixel/ rpi_ws281x library created by Jeremy Garff.

import sys
import math
import time
from bs4 import BeautifulSoup
import requests
import neopixel
import datetime as dt

TESTING = False
DEBUG = False

red = neopixel.Color(255, 0, 0)
purple = neopixel.Color(128, 0, 128)
blue = neopixel.Color(0, 0, 255)
white = neopixel.Color(255,255,255)

# LED strip configuration:
LED_COUNT = 89      # CHANGEME! Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)

# timestamp = dt.datetime.now()
# format = "%Y%m%d%H%M%S"
# s = timestamp.strftime(format)
# url = 'http://s3.amazonaws.com/origin-east-elections.politico.com/mapdata/2016/US.xml?cachebuster='+s
url = 'http://data.cnn.com/ELECTION/2016/bop/p.json'                
# print(url)                                                        
                                                                    
# Define functions which animate LEDs in various ways.
def color_wipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def reset_all(strip, wait_ms=50):
    """Set all pixels to green"""
    color_wipe(strip, purple, wait_ms)


def set_democrats(strip, electors, wait_ms=50):
    """Wipe blue in from the left side one pixel at a time."""
    # There are 538 total possible electors
    # We have LED_COUNT number of LEDs to represent them
    # So we use each LED to represent (538 / LED_COUNT) electors
    num_leds_to_change = int(electors // int(538 / LED_COUNT))
    if DEBUG:
        print("Num LEDs to change " + repr(num_leds_to_change))
    # We can represent the fractional part with the color level
    # We use modulo operator to partially light up the last LED
    remainder_level = int(electors % int(538 / LED_COUNT))
    if DEBUG:
        print("Remainder " + repr(remainder_level))
    for i in range(num_leds_to_change):
        # Turn these fully blue, one at a time
        strip.setPixelColor(i, blue)
        strip.show()
        time.sleep(wait_ms/1000.0)
    # If there is a fractional part, turn it a proportional shade
    if remainder_level > 0:
        fractional_color = int(remainder_level * 255 / 
                               int(538 / LED_COUNT))
        strip.setPixelColor(num_leds_to_change,
                            neopixel.Color(0, 0, fractional_color))
        strip.show()
        time.sleep(wait_ms/1000.0)


def set_republicans(strip, electors, wait_ms=50):
    """Wipe red in from the right side one pixel at a time."""
    num_leds_to_change = int(electors // int(538 / LED_COUNT))
    if DEBUG:
        print("Num LEDs to change " + repr(num_leds_to_change))
    # We can represent the fractional part with the color level
    # We use modulo operator to partially light up the last LED
    remainder_level = int(electors % int(538 / LED_COUNT))
    if DEBUG:
        print("Remainder " + repr(remainder_level))
    for i in range(num_leds_to_change):
        strip.setPixelColor(LED_COUNT-i, red)
        strip.show()
        time.sleep(wait_ms/1000.0)
    if remainder_level > 0:
        fractional_color = int(remainder_level * 255 / 
                               int(538 / LED_COUNT))
        strip.setPixelColor(LED_COUNT - num_leds_to_change,
                            neopixel.Color(fractional_color, 0, 0))
        strip.show()
        time.sleep(wait_ms/1000.0)

# Last results to check if the results have changed
dems_last = -1
reps_last = -1


# Main program logic follows:
if __name__ == '__main__':

    # Create NeoPixel object with appropriate configuration.
    my_strip = neopixel.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
    # Initialize the library (must be called once before other functions).
    my_strip.begin()
    # Initialize the pixels to purple
    reset_all(my_strip, 0)
    # Make the middle pixel white to show the winning line
    middle_pixel = int(math.ceil(LED_COUNT/2.)-1)
    my_strip.setPixelColor(middle_pixel, white)
    my_strip.show()
    print('Press Ctrl-C to quit.')
    while True:
        # Parse a website to find the current totals
        try:
            if DEBUG:
                print('Scrape')
            if TESTING:
                url = 'https://www.random.org/integers/?num=1&min=1&max=270&col=1&base=10&format=plain&rnd=new'
                r = requests.get(url)
                dems = r.text
                dems = int(float(dems))

                r = requests.get(url)
                reps = r.text
                reps = int(float(reps))
            else:
                r = requests.get(url)
                content = r.json()
                dems = int(content['candidates'][1]['evotes'])

                reps = int(content['candidates'][0]['evotes'])

            if (dems, reps) != (dems_last, reps_last):
                # New results, do stuff
                if DEBUG:
                    print("Dem electors " + repr(dems))
                set_democrats(my_strip, dems)
                if DEBUG:
                    print("Rep electors " + repr(reps))
                set_republicans(my_strip, reps)
                # Save the current totals for when this runs in a loop
                (dems_last, reps_last) = (dems, reps)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        if TESTING:
            time.sleep(5)
        else:
            time.sleep(5*60)
