import io
import json
import logging
from datetime import datetime
from minio import Minio
from app.config import settings
from app.routers.metrics import minio_connection_status, storage_operations

logger = logging.getLogger(__name__)

_minio_client: Minio | None = None


def set_minio_client(client: Minio) -> None:
    """Set MinIO client from main app"""
    global _minio_client
    _minio_client = client
    minio_connection_status.set(1)


async def store_temperature_data(data: dict) -> bool:
    """Store temperature data to MinIO bucket every 5min or by /store"""
    try:
        if not _minio_client:
            logger.error("MinIO client not initialized")
            minio_connection_status.set(0)
            return False
        bucket = settings.MINIO_BUCKET
        timestamp = datetime.utcnow().isoformat()
        object_name = f"temperature/{timestamp}.json"
        json_data = json.dumps(data).encode("utf-8")
        json_stream = io.BytesIO(json_data)
        _minio_client.put_object(
            bucket,
            object_name,
            data=json_stream,
            length=len(json_data),
            content_type="application/json",
        )
        storage_operations.inc()
        logger.info(f"Stored temperature data to {object_name} in bucket {bucket}")
        return True
    except Exception as e:
        logger.error(f"MinIO S3Error: {e}")
        minio_connection_status.set(0)
        return False
