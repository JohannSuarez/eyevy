#! /usr/bin/python3
from plantwatch import PlantWatch
import pathlib

if __name__ == "__main__":
    y = pathlib.Path(__file__).parent.resolve()
    print(str(y))
    x = PlantWatch()
    print(x.metadata_font_size)
    print(type(x.metadata_font_size))
    x.measured_snap()
