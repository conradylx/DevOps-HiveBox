import sys
from app.services.opensensemap import (
    OpenSenseMapError,
    fetch_box_data,
    extract_temperature_value,
    is_data_fresh,
    fetch_temperature_data,
    calculate_average_temperature,
)
from app.config.settings import settings
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


def get_sample_box_data():
    """Get sample box data with fresh timestamp"""
    return {
        "sensors": [
            {
                "title": settings.TEMPERATURE_PHENOMENON,
                "lastMeasurement": {
                    "value": "22.5",
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                },
            }
        ]
    }


@pytest.mark.asyncio
async def test_fetch_box_data_success():
    """Test successful box data fetch"""
    box_id = "test_box_123"
    expected_data = get_sample_box_data()

    mock_response = MagicMock()
    mock_response.json.return_value = expected_data
    mock_response.raise_for_status = MagicMock()

    mock_client = MagicMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await fetch_box_data(box_id)
        assert result == expected_data


@pytest.mark.asyncio
async def test_fetch_box_data_http_error():
    """Test fetch_box_data with HTTP error"""
    box_id = "test_box_123"

    mock_client = MagicMock()
    mock_client.get = AsyncMock(side_effect=httpx.HTTPError("Connection failed"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch("httpx.AsyncClient", return_value=mock_client):
        with pytest.raises(OpenSenseMapError, match="Failed to fetch box"):
            await fetch_box_data(box_id)


def test_extract_temperature_value_success():
    """Test extracting temperature from valid box data"""
    data = get_sample_box_data()
    result = extract_temperature_value(data)

    assert result is not None
    assert result["value"] == 22.5
    assert "timestamp" in result


def test_extract_temperature_value_no_sensor():
    """Test extraction when no temperature sensor exists"""
    data = {"sensors": []}
    result = extract_temperature_value(data)

    assert result is None


def test_extract_temperature_value_no_measurement():
    """Test extraction when sensor has no lastMeasurement"""
    data = {
        "sensors": [{"title": settings.TEMPERATURE_PHENOMENON, "lastMeasurement": None}]
    }
    result = extract_temperature_value(data)

    assert result is None


def test_extract_temperature_value_missing_sensors():
    """Test extraction with missing sensors key"""
    data = {}
    result = extract_temperature_value(data)

    assert result is None


def test_extract_temperature_value_wrong_title():
    """Test extraction when sensor title doesn't match"""
    data = {
        "sensors": [
            {
                "title": "Humidity",
                "lastMeasurement": {
                    "value": "50.0",
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                },
            }
        ]
    }
    result = extract_temperature_value(data)

    assert result is None


def test_is_data_fresh_recent():
    """Test that recent data is considered fresh"""
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat()

    assert is_data_fresh(timestamp) is True


def test_is_data_fresh_old():
    """Test that old data is not considered fresh"""
    old_time = datetime.now(timezone.utc) - timedelta(hours=2)
    timestamp = old_time.isoformat()

    assert is_data_fresh(timestamp) is False


def test_is_data_fresh_boundary():
    """Test data at exactly the age limit"""
    boundary_time = datetime.now(timezone.utc) - timedelta(
        seconds=settings.MAX_DATA_AGE_SECONDS - 1
    )
    timestamp = boundary_time.isoformat()

    assert is_data_fresh(timestamp) is True


def test_is_data_fresh_just_over_boundary():
    """Test data just over the age limit"""
    over_boundary = datetime.now(timezone.utc) - timedelta(
        seconds=settings.MAX_DATA_AGE_SECONDS + 1
    )
    timestamp = over_boundary.isoformat()

    assert is_data_fresh(timestamp) is False


def test_is_data_fresh_with_z_suffix():
    """Test timestamp with Z suffix (Zulu time)"""
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat().replace("+00:00", "Z")

    assert is_data_fresh(timestamp) is True


def test_calculate_average_temperature_single():
    """Test average calculation with single value"""
    data = [{"value": 22.5, "timestamp": "2024-01-01T00:00:00Z"}]

    average = calculate_average_temperature(data)
    assert average == 22.5


def test_calculate_average_temperature_multiple():
    """Test average calculation with multiple values"""
    data = [
        {"value": 20.0, "timestamp": "2024-01-01T00:00:00Z"},
        {"value": 22.0, "timestamp": "2024-01-01T00:00:00Z"},
        {"value": 24.0, "timestamp": "2024-01-01T00:00:00Z"},
    ]

    average = calculate_average_temperature(data)
    assert average == 22.0


def test_calculate_average_temperature_empty():
    """Test average calculation with empty list"""
    data = []

    average = calculate_average_temperature(data)
    assert average == 0.0


def test_calculate_average_temperature_rounding():
    """Test that average is rounded to 2 decimal places"""
    data = [
        {"value": 20.333, "timestamp": "2024-01-01T00:00:00Z"},
        {"value": 22.666, "timestamp": "2024-01-01T00:00:00Z"},
    ]

    average = calculate_average_temperature(data)
    assert average == 21.5


@pytest.mark.asyncio
async def test_fetch_temperature_data_success():
    """Test successful temperature data fetch from multiple boxes"""
    mock_box_data = get_sample_box_data()

    with patch(
        "app.services.opensensemap.fetch_box_data",
        new=AsyncMock(return_value=mock_box_data),
    ):
        result = await fetch_temperature_data()

        assert len(result) >= 1
        assert all("value" in item for item in result)
        assert all("timestamp" in item for item in result)


@pytest.mark.asyncio
async def test_fetch_temperature_data_no_fresh_data():
    """Test when no fresh data is available"""
    old_data = {
        "sensors": [
            {
                "title": settings.TEMPERATURE_PHENOMENON,
                "lastMeasurement": {
                    "value": "22.5",
                    "createdAt": (
                        datetime.now(timezone.utc) - timedelta(hours=3)
                    ).isoformat(),
                },
            }
        ]
    }

    with patch(
        "app.services.opensensemap.fetch_box_data", new=AsyncMock(return_value=old_data)
    ):
        with pytest.raises(OpenSenseMapError, match="No fresh temperature data"):
            await fetch_temperature_data()


@pytest.mark.asyncio
async def test_fetch_temperature_data_partial_failure():
    """Test when some boxes fail but others succeed"""
    fresh_data = get_sample_box_data()

    async def mock_fetch(box_id):
        if box_id == settings.SENSEBOX_IDS[0]:
            raise OpenSenseMapError("Failed")
        return fresh_data

    with patch("app.services.opensensemap.fetch_box_data", side_effect=mock_fetch):
        result = await fetch_temperature_data()
        assert len(result) >= 1


@pytest.mark.asyncio
async def test_fetch_temperature_data_all_fail():
    """Test when all boxes fail to fetch"""
    with patch(
        "app.services.opensensemap.fetch_box_data",
        side_effect=OpenSenseMapError("Failed"),
    ):
        with pytest.raises(OpenSenseMapError, match="No fresh temperature data"):
            await fetch_temperature_data()


@pytest.mark.asyncio
async def test_fetch_temperature_data_no_temperature_sensor():
    """Test when box has no temperature sensor"""
    no_temp_data = {
        "sensors": [
            {
                "title": "Humidity",
                "lastMeasurement": {
                    "value": "50.0",
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                },
            }
        ]
    }

    with patch(
        "app.services.opensensemap.fetch_box_data",
        new=AsyncMock(return_value=no_temp_data),
    ):
        with pytest.raises(OpenSenseMapError, match="No fresh temperature data"):
            await fetch_temperature_data()


def test_opensensemap_error_inheritance():
    """Test that OpenSenseMapError is an Exception"""
    error = OpenSenseMapError("Test error")
    assert isinstance(error, Exception)
    assert str(error) == "Test error"


def test_opensensemap_error_with_cause():
    """Test OpenSenseMapError raised from another exception"""
    original = ValueError("Original error")

    try:
        raise OpenSenseMapError("Wrapped error") from original
    except OpenSenseMapError as e:
        assert str(e) == "Wrapped error"
        assert e.__cause__ == original


@pytest.mark.parametrize(
    "temperature,expected_status",
    [
        pytest.param(-5.0, "Too Cold", id="freezing"),
        pytest.param(0.0, "Too Cold", id="zero"),
        pytest.param(9.9, "Too Cold", id="just_below_good"),
        pytest.param(10.0, "Good", id="lower_boundary"),
        pytest.param(20.0, "Good", id="room_temperature"),
        pytest.param(36.1, "Too Hot", id="just_above_good"),
        pytest.param(40.0, "Too Hot", id="very_hot"),
    ],
)
def test_get_temperature_status(temperature, expected_status):
    """Test temperature status determination for all ranges"""
    from app.services.opensensemap import get_temperature_status

    assert get_temperature_status(temperature) == expected_status
