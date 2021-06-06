"""
This example shows how to read the meter every 5 seconds and store data on Atlas MongoDB

Requirements:
* A cluster created on Atlas MongoDB (https://cloud.mongodb.com/)
* Updated .env file containing MONGODB_URL
* PZEM Instrument connected via USB
* The following python packages:
  $ pip install motor dnspython python-decouple

"""

from pzem import PZEM_016
from decouple import config

import motor.motor_asyncio
import time


def main() -> None:
    # Initiate DB Connection
    client = motor.motor_asyncio.AsyncIOMotorClient(config("MONGODB_URL"))
    db = client.my_game_settings  # Replace with your Cluster Name

    # Initiate PZEM-016 Meter
    pzem = PZEM_016("/dev/ttyUSB0")  # Replace with the correct path to your meter
    while True:
        print(pzem.read())
        time.sleep(5)


if __name__ == "__main__":
    main()
