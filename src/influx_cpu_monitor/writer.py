import socket
import time
from datetime import datetime, timezone

import psutil
from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from influx_cpu_monitor.config import settings
from influx_cpu_monitor.influx import make_client, ensure_bucket_exists

MEASUREMENT = "system"
HOSTNAME = socket.gethostname()


def get_temperature_c() -> float | None:
    temps = psutil.sensors_temperatures()
    if not temps:
        return None

    for sensor_name, entries in temps.items():
        if entries:
            return float(entries[0].current)

    return None


def main() -> None:
    ensure_bucket_exists()
    client = make_client()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    psutil.cpu_percent(interval=None)
    prev_disk = psutil.disk_io_counters()
    prev_time = time.time()

    while True:
        now = time.time()
        elapsed = max(now - prev_time, 0.0001)

        cpu_percent = float(psutil.cpu_percent(interval=None))

        mem = psutil.virtual_memory()

        disk = psutil.disk_io_counters()
        read_bytes_delta = disk.read_bytes - prev_disk.read_bytes
        write_bytes_delta = disk.write_bytes - prev_disk.write_bytes

        read_bps = read_bytes_delta / elapsed
        write_bps = write_bytes_delta / elapsed

        temp_c = get_temperature_c()

        point = (
            Point(MEASUREMENT)
            .tag("host", HOSTNAME)
            .field("cpu_percent", cpu_percent)
            .field("memory_percent", float(mem.percent))
            .field("memory_used_bytes", int(mem.used))
            .field("memory_available_bytes", int(mem.available))
            .field("disk_read_bytes", int(disk.read_bytes))
            .field("disk_write_bytes", int(disk.write_bytes))
            .field("disk_read_bytes_per_sec", float(read_bps))
            .field("disk_write_bytes_per_sec", float(write_bps))
            .time(datetime.now(timezone.utc), WritePrecision.MS)
        )

        if temp_c is not None:
            point = point.field("temperature_c", temp_c)

        write_api.write(bucket=settings.influxdb_bucket, record=point)

        prev_disk = disk
        prev_time = now
        time.sleep(0.1)


if __name__ == "__main__":
    main()
