import asyncio
from contextlib import asynccontextmanager
import logging

from minio import Minio
import redis.asyncio as redis
from fastapi import FastAPI

from app.config.settings import settings
from app.routers import metrics, storage, version, temperature, readyz
from app.services.minio_storage import set_minio_client, store_temperature_data
from app.routers.temperature import set_valkey_client
from app.services.opensensemap import (
    fetch_temperature_data,
    calculate_average_temperature,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("=== Initializing clients ===")
logger.info(f"MINIO_ENDPOINT: {settings.MINIO_ENDPOINT}")
logger.info(f"VALKEY_HOST: {settings.VALKEY_HOST}:{settings.VALKEY_PORT}")

try:
    minio_client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
    )
    set_minio_client(minio_client)

    if not minio_client.bucket_exists(settings.MINIO_BUCKET):
        minio_client.make_bucket(settings.MINIO_BUCKET)
        logger.info(f"✓ MinIO bucket created: {settings.MINIO_BUCKET}")
    else:
        logger.info(f"✓ MinIO bucket exists: {settings.MINIO_BUCKET}")
except Exception as e:
    logger.exception("✗ MinIO setup failed")

try:
    valkey_client = redis.Redis(
        host=settings.VALKEY_HOST, port=settings.VALKEY_PORT, decode_responses=True
    )
    set_valkey_client(valkey_client)
    logger.info(f"✓ Valkey initialized: {settings.VALKEY_HOST}:{settings.VALKEY_PORT}")
except Exception as e:
    logger.exception("✗ Valkey setup failed")


async def periodic_storage():
    await asyncio.sleep(60)
    while True:
        try:
            temp_data = await fetch_temperature_data()
            avg_temp = calculate_average_temperature(temp_data)
            await store_temperature_data(
                {
                    "average_temperature": avg_temp,
                    "samples": len(temp_data),
                }
            )
            logger.info(f"✓ Stored: {avg_temp}°C")
        except Exception as e:
            logger.warning(f"Periodic storage error: {e}")
        await asyncio.sleep(settings.STORAGE_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Cache warm-up...")
        from app.routers.temperature import get_temperature

        result = await get_temperature()
        logger.info(f"✓ Cache warmed: {result['average_temperature']}°C")
    except Exception as e:
        logger.warning(f"✗ Cache warm-up failed: {e}")

    task = asyncio.create_task(periodic_storage())
    yield
    task.cancel()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API to track environmental sensor data for beekeepers",
    lifespan=lifespan,
)

app.include_router(version.router)
app.include_router(temperature.router)
app.include_router(metrics.router)
app.include_router(readyz.router)
app.include_router(storage.router)


@app.get("/")
async def root():
    """Root endpoint - returns version."""
    return {"version": settings.VERSION}
