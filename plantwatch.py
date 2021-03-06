from dotenv import dotenv_values
from io import BytesIO
from typing import Dict, Any
from fractions import Fraction
from picamera import PiCamera
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime

import pathlib
import logging

logging.basicConfig(level=logging.INFO)

class PlantWatch:
    """
    @desc Responsibilities:
        - Pre-assess the scene to determine optimal picam parameters.
        - Load configs from env file. They include:
            - Directory location for image storage.
            - If VFLIP or HFLIP are enabled. (If camera is upsidedown or sideways)
    """

    def __init__(self):
        self.__config: Dict[str, Any] = dotenv_values(str(self.absolute_path) + '/' + '.env')
        self.save_path: str = str(self.absolute_path) + '/' + str(self.__config['SAVE_PATH'])
        self.vflip: bool = self.__config['VFLIP']
        self.hflip: bool = self.__config['HFLIP']
        self.metadata_font_size: int = int(self.__config['METADATA_FONT_SIZE'])
        self.image_data = None
        self.brightness_level: float = 0
        self.shutter_speed: float = 6_000_000

    @property
    def absolute_path(self) -> Path:
        return pathlib.Path(__file__).parent.resolve()


    @property
    def name(self) -> str:
        now = datetime.now()
        date_str: str = now.strftime("%m") + '-' + now.strftime("%d") + '-' + now.strftime("%Y")
        time_str: str = now.strftime("%H") + '-' + now.strftime("%M") + '-' + now.strftime("%S")
        return date_str + '-' + time_str


    def capture(self, shutter_speed: int = 0,
                      framerate = Fraction(30),
                      exposure_mode: str = 'auto',
                      brightness_level: float = 0,
                      iso: int = 0):
        """
        @desc Use this method with no parameters
        to get a raw, unbiased image for analysis.
        Image is stored as PIL.
        """
        # Create the in-memory stream
        stream = BytesIO()
        camera = PiCamera()

        camera.vflip = self.vflip
        camera.hflip = self.hflip
        camera.framerate = framerate
        camera.shutter_speed = shutter_speed
        camera.exposure_mode = exposure_mode
        camera.iso = iso

        camera.capture(stream, format='jpeg')


        # "Rewind" the stream to the beginning so we can
        # read its content
        stream.seek(0)
        image = Image.open(stream)
        camera.close()

        # Adding Metadata information
        draw = ImageDraw.Draw(image)
        fs: int = self.metadata_font_size

        font = ImageFont.truetype(f"{str(pathlib.Path(__file__).parent.resolve())}/fonts/Ubuntu-Regular.ttf", fs)

        draw.text((10,10), f"Framerate: {framerate}", font=font, fill=(0,255,0,255))
        draw.text((10,10 + fs), f"Shutter Speed: {shutter_speed}", font=font, fill=(0,255,0,255))
        draw.text((10,10 + fs*2), f"Brightness level: {round(brightness_level, 2)}", font=font, fill=(0,255,0,255))
        draw.text((10,10 + fs*3), f"ISO: {iso}", font=font, fill=(0,255,0,255))
        draw.text((10,10 + fs*4), f"Exposure Mode: {exposure_mode}", font=font, fill=(0,255,0,255))

        return image

    def brightness_analysis(self, image) -> None:
        """
        @desc Take image, convert to grayscale, and get the average.
        """
        logging.info(f'Conducting brightness analysis of {image}')

        im_grey = image.convert('LA')
        width, height = image.size

        total: int = 0
        for i in range(0, width):
            for j in range(0, height):
                total += im_grey.getpixel((i, j))[0]

        mean: float = total / (width * height)
        self.brightness_level = mean


    def shutter_adjustment(self, brightness_level: float) -> None:


        if  60 <= brightness_level < 200:
            logging.info(f'Image is bright, brightness level is {brightness_level}')
            self.shutter_speed = 100_000
            logging.info(f'Setting shutter speed to {self.shutter_speed}')
            return
        elif 50 <= brightness_level < 60:
            logging.info(f'Image is bright, brightness level is {brightness_level}')
            self.shutter_speed = 150_000
            logging.info(f'Setting shutter speed to {self.shutter_speed}')
            return
        elif 25 <= brightness_level < 50:
            logging.info(f'Image is dark, brightness level is {brightness_level}')
            self.shutter_speed = 200_000
            logging.info(f'Setting shutter speed to {self.shutter_speed}')
            return
        elif 10 <= brightness_level < 25:
            logging.info(f'Image is dark, brightness level is {brightness_level}')
            self.shutter_speed = 400_000
            logging.info(f'Setting shutter speed to {self.shutter_speed}')
            return
        elif 10 <= brightness_level < 3:
            logging.info(f'Image is dark, brightness level is {brightness_level}')
            self.shutter_speed = 600_000
            logging.info(f'Setting shutter speed to {self.shutter_speed}')
        elif 3 <= brightness_level < 0:
            logging.info(f'Image is dark, brightness level is {brightness_level}')
            self.shutter_speed = 6_000_000
            print(f'Setting shutter speed to {self.shutter_speed}')
            logging.info(f'Setting shutter speed to {self.shutter_speed}')
            return


    def measured_snap(self) -> None:
        """
        @desc Take initial picture, determine if too bright or too dark,
        make adjustments, then take the final picture.
        """

        self.image_data = self.capture()
        self.brightness_analysis(self.image_data)
        self.shutter_adjustment(self.brightness_level)

        image = self.capture(shutter_speed=self.shutter_speed,
                             framerate=Fraction(1,6),
                             brightness_level=self.brightness_level,
                             exposure_mode='off',
                             iso=800)

        image.save(self.save_path + '/' +  str(self.name) + '.jpg')
