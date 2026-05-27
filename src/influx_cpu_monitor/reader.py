from fastapi import FastAPI, Query

from influx_cpu_monitor.config import settings
from influx_cpu_monitor.influx import make_client

app = FastAPI(title="Influx CPU Reader")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics/cpu")
def read_cpu(seconds: int = Query(default=10, ge=1, le=3600), limit: int = Query(default=1000, ge=1, le=10000)):
    client = make_client()
    query_api = client.query_api()

    flux = f'''
from(bucket: "{settings.influxdb_bucket}")
  |> range(start: -{seconds}s)
  |> filter(fn: (r) => r._measurement == "system")
  |> filter(fn: (r) => r._field == "cpu_percent")
  |> sort(columns: ["_time"])
  |> limit(n: {limit})
'''

    tables = query_api.query(flux)
    points = []

    for table in tables:
        for record in table.records:
            points.append({
                "time": record.get_time().isoformat(),
                "value": record.get_value(),
                "host": record.values.get("host"),
            })

    return {
        "measurement": "system",
        "field": "cpu_percent",
        "seconds": seconds,
        "points": points,
    }
