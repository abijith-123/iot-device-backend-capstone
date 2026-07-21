from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: str = "development-only-key"
    database_url: str = "sqlite:///./telemetry.db"
    mqtt_enabled: bool = False
    mqtt_host: str = "broker.hivemq.com"
    mqtt_port: int = 1883
    mqtt_username: str = ""
    mqtt_password: str = ""
    mqtt_topic: str = "iot/+/telemetry"
    alert_temperature_c: float = 35.0
    alert_humidity_pct: float = 80.0
    alert_gas_ppm: float = 500.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

