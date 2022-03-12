"""
Messy script to test exposure levels on bright images
"""
#! /usr/bin/python3
from plantwatch import PlantWatch
from fractions import Fraction
from datetime import datetime
from PIL import Image

import pathlib

if __name__ == "__main__":
    '''
    First get the brightness level with an initial capture.
    Then, take 4 different pictures with different exposure levels

    TO DO:
    Code in the initial capture to get the brightness level.
    '''
    x = PlantWatch()
    now = datetime.now()

    initial_image = x.capture()
    brightness_level = x.brightness_analysis(initial_image)

    time_str = now.strftime("%H") + '-' + now.strftime("%M") + '-' + now.strftime("%S")
    shutter_speeds = [100_000, 150_000, 200_000]


    for speed in shutter_speeds:
        print(f"Writing image of {speed} exposure...")
        image = x.capture(shutter_speed=speed, framerate=Fraction(1,6), brightness_level=x.brightness_level, exposure_mode='off', iso=800)

        image.save(f'adjustment_captures/{time_str}-{speed}.jpg')


