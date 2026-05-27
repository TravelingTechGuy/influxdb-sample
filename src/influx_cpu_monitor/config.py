from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    influxdb_url: str = os.getenv("INFLUXDB_URL", "http://localhost:8086")
    influxdb_org: str = os.getenv("INFLUXDB_ORG", "local-org")
    influxdb_bucket: str = os.getenv("INFLUXDB_BUCKET", "system_metrics")
    influxdb_token: str = os.getenv("INFLUXDB_TOKEN", "local-dev-token-change-me")

settings = Settings()
