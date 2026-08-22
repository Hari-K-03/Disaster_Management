import random
import time
import json
from datetime import datetime
import requests


def generate_sensor_data():

    river_level = 2.0
    emergency_counter = 0

    while True:

        # Occasionally simulate a disaster condition
        if random.random() < 0.1:
            emergency_counter = 5

        if emergency_counter > 0:
            rainfall = random.uniform(100, 150)
            river_level += random.uniform(0.1, 0.3)
            aqi = random.randint(200, 300)
            wind_speed = random.uniform(50, 80)

            emergency_counter -= 1

        else:
            rainfall = random.uniform(0, 80)
            river_level += random.uniform(-0.1, 0.1)
            aqi = random.randint(50, 180)
            wind_speed = random.uniform(5, 40)

        temperature = random.uniform(25, 35)
        humidity = random.uniform(60, 85)

        river_level = max(0, river_level)

        reading = {
            "rainfall": round(rainfall, 2),
            "river_level": round(river_level, 2),
            "aqi": aqi,
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2),
            "wind_speed": round(wind_speed, 2),
            "timestamp": datetime.now().isoformat()
        }

        response=requests.post(
            "http://localhost:5000/sensor-data",
            json=reading
        )
        print("\nGateway response: ")
        print(response)

        time.sleep(3)


if __name__ == "__main__":
    generate_sensor_data()