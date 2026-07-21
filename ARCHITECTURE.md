# Backend Architecture

## End-to-end chain

1. The ESP32 reads temperature, humidity, and simulated gas concentration.
2. Firmware publishes one validated JSON shape to `iot/{device_id}/telemetry` every five seconds.
3. The broker decouples the device from the cloud service and delivers at QoS 1.
4. The MQTT worker validates the message and calls the same ingestion service used by HTTP.
5. The ingestion service stores the reading, evaluates every configured rule, and commits the reading and alerts together.
6. The secured REST API provides readings and alert state to Seif's dashboard.

## Component responsibilities

| Component | Responsibility | Boundary |
|---|---|---|
| ESP32 firmware | Sensor sampling, Wi-Fi/MQTT reconnect, JSON publication | Does not contain cloud secrets or alert business rules |
| MQTT broker | Topic routing and delivery decoupling | Does not validate application payloads |
| MQTT worker | Topic subscription, JSON parsing, schema validation | Rejects malformed data before storage |
| HTTP ingestion | Authenticated fallback/test ingestion | Uses the same schema and service as MQTT |
| Ingestion service | Atomic persistence and alert evaluation | Single source of write behavior |
| Alert engine | Configurable threshold comparison | Produces durable alerts rather than UI-only warnings |
| SQLite/PostgreSQL via SQLAlchemy | Readings and alerts | SQLite locally; managed PostgreSQL on Vercel |
| REST API | Secured queries and acknowledgement | Contract consumed by dashboard |

## Data model

- `telemetry_readings`: device identity, three measurements, server receive time.
- `alerts`: reading reference, device identity, rule, severity, message, value, threshold, acknowledgement, creation time.

Server receipt time is authoritative because device clocks may drift. A device `sent_at` timestamp is accepted and validated for future latency analysis but is not trusted for database ordering in this capstone.

## Security

- All `/api/v1/*` endpoints require `X-API-Key`.
- Key comparison uses constant-time comparison.
- Secrets come from environment variables and `.env` is ignored.
- Pydantic rejects impossible ranges, invalid identifiers, and naive timestamps.
- Render terminates TLS; production clients must use HTTPS.
- The public health endpoint exposes only service state, not telemetry.

For a larger system, replace a shared API key with per-device credentials/JWTs, rotate keys, enforce broker TLS, use topic ACLs, and store data in managed PostgreSQL.

## Reliability and failure handling

- Firmware reconnects to Wi-Fi and MQTT.
- QoS 1 reduces message loss but may redeliver; production should add a message ID for deduplication.
- Malformed MQTT messages are logged and rejected without stopping the worker.
- Reading and alert creation share one database transaction.
- Managed PostgreSQL prevents data loss across stateless Vercel function invocations.
- `/health` provides an external deployment check.

## Deployment boundary

Vercel runs FastAPI as an on-demand function backed by managed PostgreSQL. Because a serverless function is not a permanent process, production MQTT delivery uses a broker webhook/rule or direct authenticated HTTP from the ESP32. The included Docker deployment remains useful locally and can run the continuous MQTT worker. At scale, use a dedicated MQTT consumer service or broker rule engine and keep the API/database independently scalable.
