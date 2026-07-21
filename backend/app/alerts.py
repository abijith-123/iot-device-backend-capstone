from dataclasses import dataclass

from sqlalchemy.orm import Session

from .config import Settings
from .models import Alert, TelemetryReading


@dataclass(frozen=True)
class Rule:
    name: str
    label: str
    field: str
    threshold: float
    unit: str
    severity: str = "warning"


def configured_rules(settings: Settings) -> tuple[Rule, ...]:
    return (
        Rule("high_temperature", "Temperature", "temperature_c", settings.alert_temperature_c, "°C", "critical"),
        Rule("high_humidity", "Humidity", "humidity_pct", settings.alert_humidity_pct, "%"),
        Rule("high_gas", "Gas concentration", "gas_ppm", settings.alert_gas_ppm, "ppm", "critical"),
    )


def evaluate_alerts(db: Session, reading: TelemetryReading, settings: Settings) -> list[Alert]:
    alerts: list[Alert] = []
    for rule in configured_rules(settings):
        value = float(getattr(reading, rule.field))
        if value > rule.threshold:
            alert = Alert(
                reading_id=reading.id,
                device_id=reading.device_id,
                rule=rule.name,
                severity=rule.severity,
                message=f"{rule.label} {value:g}{rule.unit} exceeded {rule.threshold:g}{rule.unit}",
                measured_value=value,
                threshold=rule.threshold,
            )
            db.add(alert)
            alerts.append(alert)
    db.flush()
    return alerts

