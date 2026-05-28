from influxdb_client import InfluxDBClient
from influxdb_client.rest import ApiException

from influx_cpu_monitor.config import settings


def make_client() -> InfluxDBClient:
    return InfluxDBClient(
        url=settings.influxdb_url,
        token=settings.influxdb_token,
        org=settings.influxdb_org,
    )


def ensure_bucket_exists() -> None:
    client = make_client()
    buckets_api = client.buckets_api()
    orgs_api = client.organizations_api()

    orgs = orgs_api.find_organizations(org=settings.influxdb_org)
    if not orgs:
        raise RuntimeError(f"Organization not found: {settings.influxdb_org}")

    org_id = orgs[0].id
    bucket_exists = False

    try:
        buckets = buckets_api.find_buckets(name=settings.influxdb_bucket)
        if buckets and buckets.buckets:
            for bucket in buckets.buckets:
                if bucket.name == settings.influxdb_bucket:
                    bucket_exists = True
                    break
    except ApiException as e:
        if e.status != 404:
            raise

    if not bucket_exists:
        buckets_api.create_bucket(
            bucket_name=settings.influxdb_bucket,
            org_id=org_id,
            retention_rules=[]
        )
