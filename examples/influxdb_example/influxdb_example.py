from pzem import PZEM_016
from decouple import config
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO)


def main() -> None:
    influxdb_bucket = config("INFLUXDB_BUCKET")
    influxdb_org = config("INFLUXDB_ORG")
    influxdb_client = InfluxDBClient(
        url=config("INFLUXDB_URL"), token=config("INFLUXDB_TOKEN")
    )

    api = influxdb_client.write_api(write_options=SYNCHRONOUS)

    pzem = PZEM_016("/dev/ttyUSB0")  # Replace with the correct path to your meter
    while True:
        reading = pzem.read()
        timestamp = datetime.utcfromtimestamp(reading["timestamp"])

        logging.info(f"{reading}")

        # Limitation on InfluxDB to handle boolean type
        alarm_status = 1 if reading["alarm_status"] else 0

        point = (
            Point("meter_reading")
            .tag("host", "PZEM Meter")
            .field("timestamp", reading["timestamp"])
            .field("voltage", reading["voltage"])
            .field("current", reading["current"])
            .field("power", reading["power"])
            .field("energy", reading["energy"])
            .field("frequency", reading["frequency"])
            .field("power_factor", reading["power_factor"])
            .field("alarm_status", alarm_status)
            .field("alarm_threshold", reading["alarm_threshold"])
            .time(timestamp, WritePrecision.NS)
        )

        api.write(influxdb_bucket, influxdb_org, point)

        time.sleep(5)


if __name__ == "__main__":
    main()
