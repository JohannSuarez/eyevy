#! /usr/bin/python3
from plantwatch import PlantWatch
import pathlib

if __name__ == "__main__":
    y = pathlib.Path(__file__).parent.resolve()
    print(str(y))
    x = PlantWatch()
    x.measured_snap()
