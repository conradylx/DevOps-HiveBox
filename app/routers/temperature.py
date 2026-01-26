from fastapi import APIRouter, HTTPException
from app.services.opensensemap import (
    fetch_temperature_data,
    calculate_average_temperature,
    OpenSenseMapError,
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
    try:
        temperature_data = await fetch_temperature_data()
        average_temp = calculate_average_temperature(temperature_data)

        return {
            "average_temperature": average_temp,
            "unit": "°C",
            "samples": len(temperature_data),
        }

    except OpenSenseMapError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
