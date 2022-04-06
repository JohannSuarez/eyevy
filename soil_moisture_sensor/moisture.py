import time
import board

from adafruit_seesaw.seesaw import Seesaw

i2c_bus = board.I2C()

ss = Seesaw(i2c_bus, addr=0x36)

'''
To  get this sensor module working, you need CircuitPython installed.
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

After that, the sample code should work here
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
'''

while True:
	# read moisture level through capacitive touch pad
	touch = ss.moisture_read()
	
	# read temperrature from the temperature sensor
	temp = ss.get_temp()

	print(f"temp: {temp}  moisture: {touch}")
	time.sleep(1)
