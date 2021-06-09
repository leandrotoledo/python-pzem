"""
This example shows how to read the meter every 5 seconds and store data on Atlas MongoDB

Requirements:
* A cluster created on Atlas MongoDB (https://cloud.mongodb.com/)
* Updated .env file containing MONGODB_URL
* PZEM Instrument connected via USB
* The following dependencies:
  $ pip install -r examples/mongodb_example/requirements.txt

"""

from pzem import PZEM_016
from decouple import config

import motor.motor_asyncio
import time
import asyncio
import logging

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    # Initiate DB Connection
    client = motor.motor_asyncio.AsyncIOMotorClient(config("MONGODB_URL"))
    db = client.my_game_settings  # Replace with your Cluster Name
    collection = db["power_report"]  # Replace with your Collection Name

    # Initiate PZEM-016 Meter
    pzem = PZEM_016("/dev/ttyUSB0")  # Replace with the correct path to your meter
    while True:
        reading = pzem.read()
        logging.info(f"{reading}")

        await collection.insert_one(reading)

        time.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
