from datetime import datetime, timezone
from typing import List, Optional
import httpx
from app.config import settings


class OpenSenseMapError(Exception):
    """Custom exception for OpenSenseMap API errors."""

    pass


async def fetch_box_data(box_id: str) -> dict:
    """
    Fetch data for a single senseBox.

    Args:
        box_id: The senseBox ID

    Returns:
        dict: Box data from API

    Raises:
        OpenSenseMapError: If API request fails
    """
    url = f"{settings.OPENSENSEMAP_API_URL}/boxes/{box_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=15.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise OpenSenseMapError(f"Failed to fetch box {box_id}: {str(e)}") from e


def extract_temperature_value(box_data: dict) -> Optional[dict]:
    """
    Extract temperature sensor value and timestamp from box data.

    Args:
        box_data: Box data from API

    Returns:
        dict with 'value' and 'timestamp' or None if not found
    """
    sensors = box_data.get("sensors", [])

    for sensor in sensors:
        if sensor.get("title") == settings.TEMPERATURE_PHENOMENON:
            last_measurement = sensor.get("lastMeasurement")
            if last_measurement:
                return {
                    "value": float(last_measurement.get("value")),
                    "timestamp": last_measurement.get("createdAt"),
                }

    return None


def is_data_fresh(timestamp_str: str) -> bool:
    """
    Check if data is fresher than MAX_DATA_AGE_SECONDS.

    Args:
        timestamp_str: ISO format timestamp string

    Returns:
        bool: True if data is fresh
    """
    timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    age_seconds = (now - timestamp).total_seconds()

    return age_seconds <= settings.MAX_DATA_AGE_SECONDS


async def fetch_temperature_data() -> List[dict]:
    """
    Fetch temperature data from all configured senseBoxes.

    Returns:
        list: List of dicts with temperature values and timestamps

    Raises:
        OpenSenseMapError: If no valid data could be retrieved
    """
    temperature_data = []

    for box_id in settings.SENSEBOX_IDS:
        try:
            box_data = await fetch_box_data(box_id)
            temp_info = extract_temperature_value(box_data)

            if temp_info and is_data_fresh(temp_info["timestamp"]):
                temperature_data.append(temp_info)

        except OpenSenseMapError:
            continue

    if not temperature_data:
        raise OpenSenseMapError("No fresh temperature data available")

    return temperature_data


def calculate_average_temperature(temperature_data: List[dict]) -> float:
    """
    Calculate average temperature from temperature data list.

    Args:
        temperature_data: List of temperature measurements

    Returns:
        float: Average temperature rounded to 2 decimal places
    """
    if not temperature_data:
        return 0.0

    total = sum(item["value"] for item in temperature_data)
    average = total / len(temperature_data)

    return round(average, 2)
