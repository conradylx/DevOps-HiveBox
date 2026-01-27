import time
from fastapi import APIRouter, HTTPException
from app.services.opensensemap import (
    fetch_temperature_data,
    calculate_average_temperature,
    get_temperature_status,
    OpenSenseMapError,
)
from app.routers.metrics import (
    temperature_requests_counter,
    temperature_request_duration,
)

router = APIRouter()


@router.get("/temperature")
async def get_temperature():
    """
    Get current average temperature from all configured senseBoxes.

    Returns only data that is no older than 1 hour.

    Returns:
        dict: Average temperature

    Raises:
        HTTPException: If no fresh data is available
    """
    temperature_requests_counter.inc()
    start_time = time.time()

    try:
        temperature_data = await fetch_temperature_data()
        average_temp = calculate_average_temperature(temperature_data)
        status = get_temperature_status(average_temp)

        return {
            "average_temperature": average_temp,
            "unit": "°C",
            "samples": len(temperature_data),
            "status": status,
        }

    except OpenSenseMapError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    finally:
        temperature_request_duration.observe(time.time() - start_time)
