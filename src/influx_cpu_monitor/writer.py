import socket
import time
from datetime import datetime, timezone

import psutil
from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from influx_cpu_monitor.config import settings
from influx_cpu_monitor.influx import make_client

MEASUREMENT = "system"
HOSTNAME = socket.gethostname()

def main() -> None:
    client = make_client()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    psutil.cpu_percent(interval=None)

    while True:
        cpu = float(psutil.cpu_percent(interval=None))
        point = (
            Point(MEASUREMENT)
            .tag("host", HOSTNAME)
            .field("cpu_percent", cpu)
            .time(datetime.now(timezone.utc), WritePrecision.MS)
        )
        write_api.write(bucket=settings.influxdb_bucket, record=point)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
