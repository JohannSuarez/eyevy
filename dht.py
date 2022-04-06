"""
Quickly put together code to get data from DHT22
sensor and send the data to a Discord Channel webhook
"""

from dotenv import dotenv_values

import requests
import Adafruit_DHT as dht

DHT_SENSOR: int = dht.DHT22
DHT_PIN: int = 4

def grab_data() -> str:
    """
    @desc Communicate with DHT22 sensor to retreive
    humidity and temperature data
    """
    humidity, temperature = dht.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity and temperature:
        return f"Johann's Room Temperature: {round(temperature,2)}*C, Humidity={round(humidity, 1)}%"
    else:
        return "Failed to retrieve data from sensor"

def main():
    """
    @desc Invoke grab_data() from here.
    """
    # Assuming .env is in the same dir.
    url: str = dotenv_values('.env')['DISCORD_WEBHOOK_URL']

    headers: dict[str, str] = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data: str = grab_data()
    print(data)

    json_data: dict[str, str] = {
        'content': data,
    }

    response = requests.post(url, headers=headers, json=json_data)

if __name__ == "__main__":
    main()
