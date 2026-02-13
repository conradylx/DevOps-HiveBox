import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_manual_store_success():
    """Test /store endpoint successfully stores data"""
    mock_temp_data = [
        {"value": 20.0, "timestamp": "2026-02-11T10:00:00Z"},
        {"value": 22.0, "timestamp": "2026-02-11T10:05:00Z"},
    ]

    with patch(
        "app.routers.storage.fetch_temperature_data",
        new=AsyncMock(return_value=mock_temp_data),
    ):
        with patch(
            "app.routers.storage.store_temperature_data",
            new=AsyncMock(return_value=True),
        ):
            response = client.get("/store")

            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "stored" in data["message"].lower()
            assert "data" in data


@pytest.mark.asyncio
async def test_manual_store_failure():
    """Test /store endpoint when storage fails"""
    mock_temp_data = [{"value": 20.0, "timestamp": "2026-02-11T10:00:00Z"}]

    with patch(
        "app.routers.storage.fetch_temperature_data",
        new=AsyncMock(return_value=mock_temp_data),
    ):
        with patch(
            "app.routers.storage.store_temperature_data",
            new=AsyncMock(return_value=False),
        ):
            response = client.get("/store")

            assert response.status_code in [500, 503]
            assert "detail" in response.json()
