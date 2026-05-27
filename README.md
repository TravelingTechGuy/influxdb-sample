# Influx CPU Monitor

A small starter project that:
- runs InfluxDB 2 in Docker with persistent data under `./data`
- samples local CPU usage every 100ms and writes it to InfluxDB
- exposes recent samples over HTTP for a web page or dashboard

## Project layout

- `src/influx_cpu_monitor/writer.py` - writes CPU samples every 100ms
- `src/influx_cpu_monitor/reader.py` - FastAPI app that reads slices from InfluxDB
- `docker-compose.yml` - starts InfluxDB, writer, and reader
- `data/` - persistent InfluxDB storage on the host

## Initialize with uv

```bash
uv sync
```

## Start everything

```bash
docker compose up --build
```

## Services

- InfluxDB UI: http://localhost:8086
- Reader API: http://localhost:8000/metrics/cpu?seconds=10

## Example response

```json
{
  "measurement": "system",
  "field": "cpu_percent",
  "points": [
    {"time": "2026-05-27T12:00:00Z", "value": 18.4}
  ]
}
```

## Notes

- InfluxDB stores timestamps at high precision, so a 100ms cadence is fine for this starter.
- `psutil.cpu_percent(interval=None)` returns system-wide CPU usage since the last call, so the writer primes it once before entering the loop.
- Extend the same pattern for memory and temperature data.
