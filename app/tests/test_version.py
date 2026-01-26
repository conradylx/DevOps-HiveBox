import pytest
from httpx import AsyncClient, ASGITransport
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.config import settings


@pytest.fixture
async def client():
    """Test client fixture"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint returns service info."""
    response = await client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "version" in data


@pytest.mark.asyncio
async def test_version_endpoint(client):
    """Test /version endpoint returns correct version."""
    response = await client.get("/version")
    assert response.status_code == 200

    data = response.json()
    assert "version" in data
    assert isinstance(data["version"], str)


@pytest.mark.asyncio
async def test_version_format(client):
    """Test version follows semantic versioning format (X.Y.Z)."""
    response = await client.get("/version")
    version = response.json()["version"]

    if version == "unknown":
        pytest.skip("version.txt not found")

    parts = version.split(".")
    assert len(parts) == 3, f"Version should have 3 parts, got: {version}"

    for i, part in enumerate(parts):
        clean_part = part.split("-")[0]
        assert clean_part.isdigit(), f"Part {i} should be numeric, got: {part}"


@pytest.mark.asyncio
async def test_version_matches_settings(client):
    """Test version endpoint matches settings.APP_VERSION."""
    response = await client.get("/version")
    version_from_endpoint = response.json()["version"]

    version_file = Path("/code/version.txt")
    if version_file.exists():
        expected_version = version_file.read_text().strip()
    else:
        expected_version = settings.VERSION

    assert version_from_endpoint in [expected_version, "unknown"]


@pytest.mark.asyncio
async def test_version_consistency(client):
    """Test version is consistent across endpoints."""
    version_response = await client.get("/version")
    version_from_version_endpoint = version_response.json()["version"]

    root_response = await client.get("/")
    version_from_root = root_response.json()["version"]

    assert version_from_version_endpoint == version_from_root
