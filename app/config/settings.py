import os
from pathlib import Path
from typing import List


class Settings:
    """Application configuration settings."""

    @staticmethod
    def read_version() -> str:
        """Reads the application version from a file."""
        version_file = Path("/code/version.txt")

        if version_file.exists():
            return version_file.read_text(encoding="utf-8").strip()

        return "unknown"

    VERSION: str = read_version()
    APP_NAME: str = "HiveBox"

    OPENSENSEMAP_API_URL: str = "https://api.opensensemap.org"

    SENSEBOX_IDS: List[str] = os.getenv(
        "SENSEBOX_IDS",
        "5eba5fbad46fb8001b799786,5c21ff8f919bf8001adf2488,5ade1acf223bd80019a1011c",
    ).split(",")

    MAX_DATA_AGE_SECONDS: int = 3600

    TEMPERATURE_PHENOMENON: str = "Temperature"


settings = Settings()
