# Device, Ingestion, API, and Alert Contract

Base REST path: `/api/v1`  
Authentication: `X-API-Key: <secret>` on every `/api/v1/*` request.  
Content type: `application/json`.

## Telemetry object

```json
{
  "device_id": "esp32-capstone-01",
  "temperature_c": 28.4,
  "humidity_pct": 62.1,
  "gas_ppm": 214.0,
  "sent_at": "2026-07-22T12:00:00Z"
}
```

`sent_at` is optional. Valid ranges are temperature `-50..150`, humidity `0..100`, and gas `0..100000`. `device_id` accepts letters, digits, `_`, and `-`.

## MQTT

- Broker: configured through `MQTT_HOST` and `MQTT_PORT`.
- Topic: `iot/{device_id}/telemetry`.
- Subscription: `iot/+/telemetry`.
- QoS: 1.
- Payload: telemetry object above; if `device_id` is omitted, it is derived from the topic.
- Authentication/TLS: supplied by the chosen broker and injected through environment variables.

## REST endpoints

### `GET /health`

Public deployment probe. Returns `200` with `{"status":"ok", ...}`.

### `POST /api/v1/telemetry`

Stores a reading and evaluates alerts. Returns `201`:

```json
{
  "reading": {
    "id": 42,
    "device_id": "esp32-capstone-01",
    "temperature_c": 38.4,
    "humidity_pct": 62.1,
    "gas_ppm": 610,
    "received_at": "2026-07-22T12:00:01Z"
  },
  "alerts": [
    {
      "id": 9,
      "reading_id": 42,
      "device_id": "esp32-capstone-01",
      "rule": "high_temperature",
      "severity": "critical",
      "message": "Temperature 38.4°C exceeded 35°C",
      "measured_value": 38.4,
      "threshold": 35,
      "acknowledged": false,
      "created_at": "2026-07-22T12:00:01Z"
    }
  ]
}
```

### `GET /api/v1/readings`

Query parameters: optional `device_id`; `limit` from 1 to 500 (default 100). Returns newest first.

### `GET /api/v1/alerts`

Query parameters: optional `device_id`, optional `acknowledged=true|false`, and `limit` from 1 to 500. Returns newest first.

### `PATCH /api/v1/alerts/{alert_id}/acknowledge`

Marks one alert acknowledged. Returns the updated alert or `404`.

## Alert rules

| Rule | Default trigger | Severity | Environment variable |
|---|---:|---|---|
| `high_temperature` | temperature > 35°C | critical | `ALERT_TEMPERATURE_C` |
| `high_humidity` | humidity > 80% | warning | `ALERT_HUMIDITY_PCT` |
| `high_gas` | gas > 500 ppm | critical | `ALERT_GAS_PPM` |

The comparison is strictly greater than the threshold. One reading can generate multiple alerts. Alerts remain available until acknowledged; acknowledgement is an audit state and does not delete an alert.

## Errors

- `401`: missing or invalid key.
- `404`: alert does not exist.
- `422`: JSON or query validation failed.
- `500`: unexpected server error; clients may retry with backoff.

