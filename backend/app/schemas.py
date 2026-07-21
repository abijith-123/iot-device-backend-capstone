from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TelemetryIn(BaseModel):
    device_id: str = Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9_-]+$")
    temperature_c: float = Field(ge=-50, le=150)
    humidity_pct: float = Field(ge=0, le=100)
    gas_ppm: float = Field(ge=0, le=100000)
    sent_at: datetime | None = None

    @field_validator("sent_at")
    @classmethod
    def timestamp_must_be_timezone_aware(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("sent_at must include a timezone")
        return value


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reading_id: int
    device_id: str
    rule: str
    severity: str
    message: str
    measured_value: float
    threshold: float
    acknowledged: bool
    created_at: datetime


class TelemetryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: str
    temperature_c: float
    humidity_pct: float
    gas_ppm: float
    received_at: datetime


class IngestResult(BaseModel):
    reading: TelemetryOut
    alerts: list[AlertOut]


class HealthOut(BaseModel):
    status: str
    service: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

