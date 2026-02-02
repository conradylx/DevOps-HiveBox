from fastapi import APIRouter, Response
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
    REGISTRY,
    Gauge,
)

router = APIRouter(tags=["metrics"])

temperature_requests_counter = Counter(
    "hivebox_temperature_requests_total",
    "Total number of temperature requests",
    registry=REGISTRY,
)

temperature_cache_hits = Counter(
    "hivebox_temperature_cache_hits_total",
    "Total number of cache hits for temperature data",
    registry=REGISTRY,
)

storage_operations = Counter(
    "hivebox_storage_operations_total",
    "Total number of storage operations",
    registry=REGISTRY,
)

valkey_connection_status = Gauge(
    "hivebox_valkey_connected",
    "Valkey connection status (1 for connected, 0 for disconnected)",
    registry=REGISTRY,
)

minio_connection_status = Gauge(
    "hivebox_minio_connected",
    "MinIO connection status (1 for connected, 0 for disconnected)",
    registry=REGISTRY,
)

sensebox_available = Gauge(
    "hivebox_sensebox_available",
    "SenseBox availability status (1 for available, 0 for unavailable)",
    registry=REGISTRY,
)

temperature_value = Gauge(
    "hivebox_temperature_celsius",
    "Current temperature in Celsius",
    registry=REGISTRY,
)

api_request_duration = Histogram(
    "hivebox_api_request_duration_seconds",
    "Duration of API requests in seconds",
    registry=REGISTRY,
)

temperature_cache_misses = Counter(
    "hivebox_temperature_cache_misses_total",
    "Total number of cache misses for temperature data",
    registry=REGISTRY,
)

temperature_request_duration = Histogram(
    "hivebox_temperature_request_duration_seconds",
    "Duration of temperature requests in seconds",
    registry=REGISTRY,
)

version_requests_counter = Counter(
    "hivebox_version_requests_total",
    "Total number of version requests",
    registry=REGISTRY,
)


@router.get("/metrics")
async def get_metrics():
    """
    Prometheus metrics endpoint
    Returns all default and custom metrics in Prometheus format
    """
    metrics_output = generate_latest(REGISTRY)
    return Response(content=metrics_output, media_type=CONTENT_TYPE_LATEST)
