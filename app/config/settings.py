import os
from pathlib import Path


class Settings:
    """Application configuration settings."""

    def __init__(self):
        version_file = Path("/code/version.txt")
        if version_file.exists():
            self.VERSION = version_file.read_text(encoding="utf-8").strip()
        else:
            self.VERSION = os.getenv("VERSION", "unknown")

        self.APP_NAME = "HiveBox"

        self.OPENSENSEMAP_API_URL = os.getenv(
            "OPENSENSEMAP_API_URL", "https://api.opensensemap.org"
        )
        sensebox_ids_str = os.getenv(
            "SENSEBOX_IDS",
            "5eba5fbad46fb8001b799786,5c21ff8f919bf8001adf2488,5ade1acf223bd80019a1011c",
        )
        self.SENSEBOX_IDS = [id.strip() for id in sensebox_ids_str.split(",")]
        self.MAX_DATA_AGE_SECONDS = int(os.getenv("MAX_DATA_AGE_SECONDS", "3600"))
        self.TEMPERATURE_PHENOMENON = os.getenv("TEMPERATURE_PHENOMENON", "Temperatur")

        self.VALKEY_HOST = os.getenv("VALKEY_HOST", "localhost")
        self.VALKEY_PORT = int(os.getenv("VALKEY_PORT", "6379"))
        self.CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))

        self.MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.MINIO_BUCKET = os.getenv("MINIO_BUCKET", "hivebox")
        self.MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"

        self.STORAGE_INTERVAL = int(os.getenv("STORAGE_INTERVAL", "300"))


settings = Settings()
