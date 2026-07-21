from sqlalchemy.orm import Session

from .alerts import evaluate_alerts
from .config import Settings
from .models import Alert, TelemetryReading
from .schemas import TelemetryIn


def ingest_telemetry(db: Session, payload: TelemetryIn, settings: Settings) -> tuple[TelemetryReading, list[Alert]]:
    reading = TelemetryReading(
        device_id=payload.device_id,
        temperature_c=payload.temperature_c,
        humidity_pct=payload.humidity_pct,
        gas_ppm=payload.gas_ppm,
    )
    db.add(reading)
    db.flush()
    alerts = evaluate_alerts(db, reading, settings)
    db.commit()
    db.refresh(reading)
    for alert in alerts:
        db.refresh(alert)
    return reading, alerts

