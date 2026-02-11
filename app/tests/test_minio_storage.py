import pytest
from unittest.mock import MagicMock, patch
from app.services.minio_storage import set_minio_client, store_temperature_data


def test_set_minio_client():
    """Test setting MinIO client"""
    mock_client = MagicMock()
    set_minio_client(mock_client)

    from app.services.minio_storage import _minio_client

    assert _minio_client is not None


@pytest.mark.asyncio
async def test_store_temperature_data_success():
    """Test successful data storage"""
    mock_client = MagicMock()
    mock_client.put_object.return_value = None

    with patch("app.services.minio_storage._minio_client", mock_client):
        result = await store_temperature_data({"temperature": 20.5})
        assert result is True
        mock_client.put_object.assert_called_once()


@pytest.mark.asyncio
async def test_store_temperature_data_no_client():
    """Test storage when client not initialized"""
    with patch("app.services.minio_storage._minio_client", None):
        result = await store_temperature_data({"temperature": 20.5})
        assert result is False
