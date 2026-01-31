from fastapi import APIRouter, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

router = APIRouter()

temperature_requests_counter = Counter(
    "hivebox_temperature_requests_total", "Total number of temperature requests"
)

temperature_request_duration = Histogram(
    "hivebox_temperature_request_duration_seconds",
    "Duration of temperature requests in seconds",
)

version_requests_counter = Counter(
    "hivebox_version_requests_total", "Total number of version requests"
)


@router.get("/metrics")
async def get_metrics():
    """
    Get Prometheus metrics.

    Returns:
        Response: Prometheus metrics in text format
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
