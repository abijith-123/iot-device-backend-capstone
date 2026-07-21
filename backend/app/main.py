from contextlib import asynccontextmanager
from datetime import datetime, timezone
from secrets import compare_digest

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import Settings, get_settings
from .database import Base, engine, get_db
from .models import Alert, TelemetryReading
from .mqtt_worker import MqttWorker
from .schemas import AlertOut, HealthOut, IngestResult, TelemetryIn, TelemetryOut
from .service import ingest_telemetry


def require_api_key(
    x_api_key: str | None = Header(default=None), settings: Settings = Depends(get_settings)
) -> None:
    if not x_api_key or not compare_digest(x_api_key, settings.api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    settings = get_settings()
    worker = MqttWorker(settings) if settings.mqtt_enabled else None
    if worker:
        worker.start()
    app.state.mqtt_worker = worker
    yield
    if worker:
        worker.stop()


app = FastAPI(
    title="IoT Device & Alert API",
    version="1.0.0",
    description="Secured HTTP/MQTT telemetry ingestion, storage, querying, and threshold alerts.",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthOut, tags=["operations"])
def health() -> HealthOut:
    return HealthOut(status="ok", service="iot-device-backend")


@app.post(
    "/api/v1/telemetry",
    response_model=IngestResult,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
    tags=["telemetry"],
)
def create_telemetry(
    payload: TelemetryIn,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> IngestResult:
    reading, alerts = ingest_telemetry(db, payload, settings)
    return IngestResult(reading=reading, alerts=alerts)


@app.get(
    "/api/v1/readings",
    response_model=list[TelemetryOut],
    dependencies=[Depends(require_api_key)],
    tags=["telemetry"],
)
def list_readings(
    device_id: str | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[TelemetryReading]:
    statement = select(TelemetryReading)
    if device_id:
        statement = statement.where(TelemetryReading.device_id == device_id)
    statement = statement.order_by(TelemetryReading.received_at.desc()).limit(limit)
    return list(db.scalars(statement))


@app.get(
    "/api/v1/alerts",
    response_model=list[AlertOut],
    dependencies=[Depends(require_api_key)],
    tags=["alerts"],
)
def list_alerts(
    device_id: str | None = None,
    acknowledged: bool | None = None,
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[Alert]:
    statement = select(Alert)
    if device_id:
        statement = statement.where(Alert.device_id == device_id)
    if acknowledged is not None:
        statement = statement.where(Alert.acknowledged == acknowledged)
    statement = statement.order_by(Alert.created_at.desc()).limit(limit)
    return list(db.scalars(statement))


@app.patch(
    "/api/v1/alerts/{alert_id}/acknowledge",
    response_model=AlertOut,
    dependencies=[Depends(require_api_key)],
    tags=["alerts"],
)
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)) -> Alert:
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    alert.acknowledged = True
    db.commit()
    db.refresh(alert)
    return alert

