from influxdb_client import InfluxDBClient
from influx_cpu_monitor.config import settings

def make_client() -> InfluxDBClient:
    return InfluxDBClient(
        url=settings.influxdb_url,
        token=settings.influxdb_token,
        org=settings.influxdb_org,
    )
