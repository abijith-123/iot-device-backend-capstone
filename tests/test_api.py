import os
from pathlib import Path

TEST_DB = Path("test_telemetry.db")
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["API_KEY"] = "test-secret"
os.environ["MQTT_ENABLED"] = "false"

from fastapi.testclient import TestClient

from backend.app.database import Base, _runtime_database_url, engine
from backend.app.main import app


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module():
    engine.dispose()
    TEST_DB.unlink(missing_ok=True)


def test_health_is_public():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_vercel_sqlite_fallback_uses_writable_tmp(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    assert _runtime_database_url("sqlite:///./telemetry.db") == "sqlite:////tmp/telemetry.db"
    assert _runtime_database_url("postgresql://example/db") == "postgresql://example/db"


def test_telemetry_requires_authentication():
    with TestClient(app) as client:
        response = client.post("/api/v1/telemetry", json={})
    assert response.status_code == 401


def test_ingestion_persists_reading_and_creates_alerts():
    payload = {
        "device_id": "esp32-test",
        "temperature_c": 38.5,
        "humidity_pct": 61.2,
        "gas_ppm": 650,
    }
    headers = {"X-API-Key": "test-secret"}
    with TestClient(app) as client:
        created = client.post("/api/v1/telemetry", json=payload, headers=headers)
        readings = client.get("/api/v1/readings", headers=headers)
        alerts = client.get("/api/v1/alerts?acknowledged=false", headers=headers)

    assert created.status_code == 201
    assert {alert["rule"] for alert in created.json()["alerts"]} == {"high_temperature", "high_gas"}
    assert readings.json()[0]["device_id"] == "esp32-test"
    assert len(alerts.json()) == 2


def test_alert_can_be_acknowledged():
    headers = {"X-API-Key": "test-secret"}
    payload = {"device_id": "esp32-test", "temperature_c": 20, "humidity_pct": 90, "gas_ppm": 100}
    with TestClient(app) as client:
        created = client.post("/api/v1/telemetry", json=payload, headers=headers).json()
        alert_id = created["alerts"][0]["id"]
        response = client.patch(f"/api/v1/alerts/{alert_id}/acknowledge", headers=headers)
    assert response.status_code == 200
    assert response.json()["acknowledged"] is True
