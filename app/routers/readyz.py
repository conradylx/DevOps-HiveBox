import json
import logging
from fastapi import APIRouter, Response

from app.services.opensensemap import check_senseboxes_availability

logger = logging.getLogger(__name__)
router = APIRouter(tags=["readiness"])


def get_valkey_client():
    """Get Valkey client dynamically"""
    from app.routers.temperature import _valkey_client

    return _valkey_client


@router.get("/healthz")
async def healthz():
    """
    Liveness probe endpoint for Kubernetes.
    Returns 200 if app is alive (can handle requests).
    """
    return {"status": "healthy"}


@router.get("/readyz")
async def readyz():
    """
    Kubernetes readiness probe

    Returns HTTP 200 only if:
    - Less than 50% of senseBoxes are unavailable
    - AND cache is not older than 5 minutes
    """
    reasons = []
    valkey_status = "unknown"
    minio_status = "unknown"

    try:
        senseboxes_available, senseboxes_total = await check_senseboxes_availability()
        unavailable_ratio = (
            ((senseboxes_total - senseboxes_available) / senseboxes_total) * 100
            if senseboxes_total > 0
            else 100
        )
        if unavailable_ratio >= 50:
            reasons.append(
                f"SenseBox availability below threshold: {senseboxes_available}/{senseboxes_total} available"
            )
    except Exception as e:
        logger.error(f"Error checking senseBoxes: {e}")
        reasons.append("Failed to check senseBoxes availability")

    cache_valid = False
    valkey_client = get_valkey_client()

    if valkey_client:
        try:
            valkey_status = "connected"
            cached_data = await valkey_client.get("temperature_data")
            if cached_data:
                ttl = await valkey_client.ttl("temperature_data")
                if ttl > 0:
                    cache_valid = True
                else:
                    reasons.append("Cache expired (TTL <= 0)")
            else:
                reasons.append("No cached temperature data")
        except Exception as e:
            logger.error(f"Error checking cache: {e}")
            reasons.append("Failed to check cache")
            valkey_status = "disconnected"
    else:
        reasons.append("Valkey client not initialized")

    try:
        from app.services.minio_storage import _minio_client

        if _minio_client is not None:
            _minio_client.list_buckets()
            minio_status = "connected"
        else:
            minio_status = "disconnected"
            reasons.append("MinIO client not initialized")
    except Exception as e:
        logger.error(f"Error checking MinIO: {e}")
        minio_status = "disconnected"

    if not reasons and cache_valid:
        return {
            "status": "ready",
            "valkey": "connected",
            "minio": "connected",
            "checks": {"senseBoxes": "ok", "cache": "ok"},
        }

    logger.warning(f"Readiness check failed: {', '.join(reasons)}")
    return Response(
        content=json.dumps(
            {
                "status": "not ready",
                "valkey": valkey_status,
                "minio": minio_status,
                "reasons": reasons,
            }
        ),
        status_code=503,
        media_type="application/json",
    )
