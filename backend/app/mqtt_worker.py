import json
import logging
import threading

import paho.mqtt.client as mqtt
from pydantic import ValidationError

from .config import Settings
from .database import SessionLocal
from .schemas import TelemetryIn
from .service import ingest_telemetry

logger = logging.getLogger(__name__)


class MqttWorker:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="iot-ingestion-api")
        if settings.mqtt_username:
            self.client.username_pw_set(settings.mqtt_username, settings.mqtt_password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self._thread: threading.Thread | None = None

    def _on_connect(self, client, _userdata, _flags, reason_code, _properties) -> None:
        if reason_code == 0:
            client.subscribe(self.settings.mqtt_topic, qos=1)
            logger.info("Subscribed to %s", self.settings.mqtt_topic)
        else:
            logger.error("MQTT connection failed: %s", reason_code)

    def _on_message(self, _client, _userdata, message) -> None:
        try:
            data = json.loads(message.payload.decode("utf-8"))
            topic_device = message.topic.split("/")[1]
            data.setdefault("device_id", topic_device)
            payload = TelemetryIn.model_validate(data)
            with SessionLocal() as db:
                ingest_telemetry(db, payload, self.settings)
        except (json.JSONDecodeError, UnicodeDecodeError, ValidationError, IndexError) as exc:
            logger.warning("Rejected MQTT message on %s: %s", message.topic, exc)
        except Exception:
            logger.exception("Unexpected MQTT ingestion failure")

    def start(self) -> None:
        self.client.connect_async(self.settings.mqtt_host, self.settings.mqtt_port, keepalive=60)
        self.client.loop_start()

    def stop(self) -> None:
        self.client.disconnect()
        self.client.loop_stop()

