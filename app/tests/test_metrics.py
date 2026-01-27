from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_metrics_endpoint_exists():
    """Test that /metrics endpoint exists."""
    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_content_type():
    """Test that /metrics returns Prometheus format."""
    response = client.get("/metrics")
    assert "text/plain" in response.headers["content-type"]


def test_metrics_contains_default_metrics():
    """Test that /metrics contains default Prometheus metrics."""
    response = client.get("/metrics")
    content = response.text

    assert "process_cpu_seconds_total" in content or "python_info" in content


def test_metrics_increments_on_version_call():
    """Test that version requests are counted."""
    client.get("/version")

    response = client.get("/metrics")
    content = response.text

    assert "hivebox_version_requests_total" in content


def test_metrics_increments_on_temperature_call():
    """Test that temperature requests are counted."""
    client.get("/temperature")

    response = client.get("/metrics")
    content = response.text

    assert "hivebox_temperature_requests_total" in content
