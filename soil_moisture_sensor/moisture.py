"""
To get this sensor module working, you need CircuitPython installed.
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

After that, the sample code from here should work:
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
"""

import time
import requests
import statistics
import board

from adafruit_seesaw.seesaw import Seesaw

i2c_bus = board.I2C()

ss = Seesaw(i2c_bus, addr=0x36)

def grab_temp() -> float:
    """
    @desc Read temperature (Accurate by +-2*C)
    """
    return ss.get_temp()

def grab_moisture() -> float:
    """
    @desc Read moisture (Always recalibrate everytime you replant this sensor)
    """
    return ss.moisture_read()


def main():

    url: str = 'https://discord.com/api/webhooks/945755701760909352/jW8tKjVsDUxX4_fLzgX8-WO6SIyu5ozMz2cVxKfi4oCpd9IOfUHR5PO36mk-QCcuBz-U'

    data: float | str

    headers: dict[str, str] = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            }

    reading_collection: List[float] = []
    for i in range(10):
        moisture: float = grab_moisture()
        # print(moisture)
        reading_collection.append(moisture)
        time.sleep(1)
    
    try:
        data = statistics.fmean(reading_collection)
        # print(f"Test Soil moisture reading: {data}")
    except Exception as e:
        data = "Reading failed."

    json_data = {
        'content': f"Soil Moisture Reading: {str(data)}"
    }

    response = requests.post(url, headers=headers, json=json_data)

if __name__ == "__main__":
    main()
