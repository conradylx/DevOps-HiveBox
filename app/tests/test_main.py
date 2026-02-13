import pytest
from unittest.mock import AsyncMock, patch
from app.main import app


def test_root_endpoint():
    """Test root endpoint returns version"""
    from fastapi.testclient import TestClient

    client = TestClient(app)

    response = client.get("/")
    assert response.status_code == 200
    assert "version" in response.json()


@pytest.mark.asyncio
async def test_lifespan_startup():
    """Test lifespan startup - cache warmup"""
    with patch(
        "app.routers.temperature.get_temperature",
        new=AsyncMock(return_value={"average_temperature": 20.5}),
    ):
        pass
