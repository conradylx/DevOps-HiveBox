import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.services.opensensemap import (
    extract_temperature_value,
    is_data_fresh,
    calculate_average_temperature,
    fetch_temperature_data,
    OpenSenseMapError,
)


client = TestClient(app)


SAMPLE_BOX_DATA = {
    "sensors": [
        {
            "title": "Temperatur",
            "lastMeasurement": {
                "value": "22.5",
                "createdAt": datetime.now(timezone.utc).isoformat(),
            },
        }
    ]
}


def test_extract_temperature_value():
    """Test extracting temperature from box data."""
    result = extract_temperature_value(SAMPLE_BOX_DATA)
    assert result is not None
    assert result["value"] == 22.5
    assert "timestamp" in result


def test_extract_temperature_no_sensor():
    """Test extraction when no temperature sensor exists."""
    data = {"sensors": []}
    result = extract_temperature_value(data)
    assert result is None


def test_is_data_fresh():
    """Test data freshness check with recent timestamp."""
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat()
    assert is_data_fresh(timestamp) is True


def test_is_data_old():
    """Test data freshness check with old timestamp."""
    old_time = datetime.now(timezone.utc) - timedelta(hours=2)
    timestamp = old_time.isoformat()
    assert is_data_fresh(timestamp) is False


def test_calculate_average_temperature():
    """Test average temperature calculation."""
    data = [
        {"value": 20.0, "timestamp": "2024-01-01T00:00:00Z"},
        {"value": 22.0, "timestamp": "2024-01-01T00:00:00Z"},
        {"value": 24.0, "timestamp": "2024-01-01T00:00:00Z"},
    ]
    average = calculate_average_temperature(data)
    assert average == 22.0


def test_calculate_average_empty_list():
    """Test average calculation with empty list."""
    average = calculate_average_temperature([])
    assert average == 0.0


@pytest.mark.asyncio
async def test_fetch_temperature_data_success():
    """Test successful temperature data fetch."""
    mock_data = SAMPLE_BOX_DATA.copy()
    with patch(
        "app.services.opensensemap.fetch_box_data",
        new=AsyncMock(return_value=mock_data),
    ):
        result = await fetch_temperature_data()
        assert len(result) > 0
        assert all("value" in item for item in result)


@pytest.mark.asyncio
async def test_fetch_temperature_data_no_fresh_data():
    """Test when no fresh data is available."""
    old_data = {
        "sensors": [
            {
                "title": "Temperatur",
                "lastMeasurement": {
                    "value": "22.5",
                    "createdAt": (
                        datetime.now(timezone.utc) - timedelta(hours=2)
                    ).isoformat(),
                },
            }
        ]
    }
    with patch(
        "app.services.opensensemap.fetch_box_data", new=AsyncMock(return_value=old_data)
    ):
        with pytest.raises(OpenSenseMapError):
            await fetch_temperature_data()


def test_temperature_endpoint_success():
    """Test /temperature endpoint returns 200 with correct data."""
    mock_data = [
        {"value": 20.0, "timestamp": "2024-01-01T00:00:00Z"},
        {"value": 22.0, "timestamp": "2024-01-01T00:00:00Z"},
    ]
    with patch(
        "app.routers.temperature.fetch_temperature_data",
        new=AsyncMock(return_value=mock_data),
    ):
        response = client.get("/temperature")
        assert response.status_code == 200
        data = response.json()
        assert "average_temperature" in data
        assert "unit" in data
        assert "samples" in data
        assert data["unit"] == "°C"
        assert data["samples"] == 2


def test_temperature_endpoint_opensensemap_error():
    """Test /temperature endpoint when OpenSenseMapError occurs."""
    with patch(
        "app.routers.temperature.fetch_temperature_data",
        side_effect=OpenSenseMapError("No fresh data"),
    ):
        response = client.get("/temperature")
        assert response.status_code == 503
        assert "detail" in response.json()
