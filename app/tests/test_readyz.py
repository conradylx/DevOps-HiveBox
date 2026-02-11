import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_healthz_endpoint():
    """Test /healthz returns healthy status"""
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_readyz_success():
    """Test /readyz when all services are ready"""
    with patch(
        "app.routers.readyz.check_senseboxes_availability",
        new=AsyncMock(return_value=(3, 3)),
    ):
        with patch("app.routers.readyz.get_valkey_client") as mock_valkey:
            mock_client = AsyncMock()
            mock_client.get.return_value = '{"test": "data"}'
            mock_client.ttl.return_value = 100
            mock_valkey.return_value = mock_client

            with patch("app.services.minio_storage._minio_client") as mock_minio:
                mock_minio.list_buckets.return_value = []

                response = client.get("/readyz")
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "ready"
                assert data["valkey"] == "connected"
                assert data["minio"] == "connected"


def test_readyz_not_ready():
    """Test /readyz when services are not ready"""
    with patch(
        "app.routers.readyz.check_senseboxes_availability",
        new=AsyncMock(return_value=(0, 3)),
    ):
        response = client.get("/readyz")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not ready"


def test_readyz_valkey_disconnected():
    """Test /readyz when Valkey is down"""
    with patch(
        "app.routers.readyz.check_senseboxes_availability",
        new=AsyncMock(return_value=(3, 3)),
    ):
        with patch("app.routers.readyz.get_valkey_client", return_value=None):
            response = client.get("/readyz")
            assert response.status_code == 503
            data = response.json()
            assert data["valkey"] == "unknown" or "disconnected" in str(data)


def test_readyz_cache_expired():
    """Test /readyz when cache TTL is negative"""
    with patch(
        "app.routers.readyz.check_senseboxes_availability",
        new=AsyncMock(return_value=(3, 3)),
    ):
        with patch("app.routers.readyz.get_valkey_client") as mock_valkey:
            mock_client = AsyncMock()
            mock_client.get.return_value = '{"test": "data"}'
            mock_client.ttl.return_value = -1
            mock_valkey.return_value = mock_client

            response = client.get("/readyz")
            assert response.status_code == 503
