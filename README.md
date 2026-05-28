# Influx CPU Monitor

A small starter project that:
- runs InfluxDB 2 in Docker with persistent data under `./data`
- samples local CPU usage, memory usage, disk usage, and temperature (only on systems that allow it - i.e. not MacOS) every 100ms and writes it to InfluxDB
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
- Reader API:
  - http://localhost:8000/health - general health of the systems
  - http://localhost:8000/metrics?field=cpu_percent&seconds=10
  - http://localhost:8000/metrics?field=memory_percent&seconds=30
  - http://localhost:8000/metrics?field=disk_read_bytes_per_sec&seconds=30
  - http://localhost:8000/metrics?field=temperature_c&seconds=300 - may return empty, depending on your OS

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

# Sample client

`client_example.py` demonstrates consuming data from the reader. Run it using `python3 src/influx_cpu_monitor/client_example.py` from the root of the project.

## Notes

- InfluxDB stores timestamps at high precision, so a 100ms cadence is fine for this starter.
- `psutil.cpu_percent(interval=None)` returns system-wide CPU usage since the last call, so the writer primes it once before entering the loop.

