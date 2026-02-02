import json
import logging
import time
from fastapi import APIRouter, HTTPException
import redis.asyncio as redis
from app.config import settings
from app.services.opensensemap import (
    fetch_temperature_data,
    calculate_average_temperature,
    get_temperature_status,
    OpenSenseMapError,
)
from app.routers.metrics import (
    temperature_requests_counter,
    temperature_request_duration,
    temperature_cache_hits,
    temperature_cache_misses,
    temperature_value,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["temperature"])

router = APIRouter(tags=["temperature"])

_valkey_client: redis.Redis | None = None


def set_valkey_client(client: redis.Redis) -> None:
    """Set Valkey client from main app"""
    global _valkey_client
    _valkey_client = client


@router.get("/temperature")
async def get_temperature():
    """
    Get average temperature from configured senseBoxes

    - Data must be no older than 1 hour
    - Uses Valkey cache (5 minute TTL)
    - Returns temperature with status based on thresholds
    - Increments Prometheus metrics
    """
    temperature_requests_counter.inc()
    start_time = time.time()

    cache_key = "temperature_data"

    try:
        if _valkey_client:
            try:
                cached_data = await _valkey_client.get(cache_key)
                if cached_data:
                    temperature_cache_hits.inc()
                    cached_result = json.loads(cached_data)
                    temperature_value.set(cached_result["average_temperature"])
                    return cached_result
            except redis.RedisError as e:
                logger.warning(f"Cache read error: {e}")

        temperature_cache_misses.inc()
        logger.info("Fetching temperature data from OpenSenseMap")
        temperature_data = await fetch_temperature_data()
        average_temperature = calculate_average_temperature(temperature_data)
        status = get_temperature_status(average_temperature)

        result = {
            "average_temperature": average_temperature,
            "status": status,
            "unit": "°C",
            "samples": len(temperature_data),
        }

        if _valkey_client:
            try:
                await _valkey_client.setex(
                    cache_key, settings.CACHE_TTL, json.dumps(result)
                )
                logger.info("Temperature data cached successfully")
            except redis.RedisError as e:
                logger.warning(f"Cache write error: {e}")

        temperature_value.set(average_temperature)
        return result

    except OpenSenseMapError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    finally:
        temperature_request_duration.observe(time.time() - start_time)
