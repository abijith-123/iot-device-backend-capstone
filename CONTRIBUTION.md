# Individual Contribution Showcase — Abijith Biju

## Layer I Owned

I owned the complete **device-to-backend data chain**:

**ESP32 firmware → MQTT/HTTP ingestion → validation → database persistence → secured REST API → automatic alert generation**

My responsibility was to collect sensor values, transfer them to the backend, validate and store them, check for dangerous readings, and make the results available through authenticated API endpoints. My contribution ends at the documented API contract. The external dashboard and frontend implementation are outside the work claimed here.

## What I Personally Developed

### ESP32 Firmware

I developed the ESP32 firmware used to collect temperature, humidity, and simulated gas readings. The firmware connects to Wi-Fi, reads the DHT22 and gas input, creates a JSON telemetry message, publishes every five seconds, uses the topic `iot/esp32-capstone-01/telemetry`, and prints each payload to the Serial Monitor for visible testing.

### Telemetry Ingestion

I created two supported ingestion paths. The MQTT worker receives IoT messages, while the authenticated HTTP endpoint supports production delivery, testing, broker webhooks, and direct device requests. Both paths use the same validation and storage service so that the backend behaves consistently.

### Validation and Security

I used Pydantic schemas to reject invalid device IDs, impossible sensor ranges, malformed JSON, and unsuitable timestamps. All `/api/v1/*` endpoints are protected using an `X-API-Key` header. The production key is stored in Vercel environment variables and is not committed to GitHub.

### Database and Persistence

I created the telemetry and alert database models using SQLAlchemy. SQLite is used locally and during testing, while Neon PostgreSQL provides durable storage for the deployed Vercel backend. A reading and its related alerts are committed through the same ingestion process.

### Alert Engine

I developed configurable rules for high temperature, high humidity, and high gas readings. The default thresholds are 35°C, 80% humidity, and 500 ppm gas. One reading can generate multiple alerts, and each alert keeps its rule, severity, value, threshold, message, time, and acknowledgement status.

### Backend API

I implemented:

- `GET /health`
- `POST /api/v1/telemetry`
- `GET /api/v1/readings`
- `GET /api/v1/alerts`
- `PATCH /api/v1/alerts/{alert_id}/acknowledge`

### Deployment, Testing, and Documentation

I adapted the backend for Vercel, connected Neon PostgreSQL, corrected dependency and serverless-storage problems, added Pytest tests, added GitHub Actions CI, maintained Docker/local setup files, and completed the architecture, protocol, contribution, and walkthrough documentation.

## Evidence

- Repository: https://github.com/abijith-123/iot-device-backend-capstone
- Final main branch: https://github.com/abijith-123/iot-device-backend-capstone/tree/main
- Main implementation PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/1
- Vercel adaptation PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/2
- Dependency fix PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/3
- Runtime-storage fix PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/4
- Deployment evidence PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/5
- Neon verification PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/6
- Simulator and walkthrough PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/8
- Backend CI evidence PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/9
- Final internship reflection: https://github.com/abijith-123/iot-device-backend-capstone/blob/main/FINAL_INTERNSHIP_REFLECTION.md
- Live health endpoint: https://iot-device-backend-capstone.vercel.app/health
- Live API docs: https://iot-device-backend-capstone.vercel.app/docs
- Live Wokwi simulation: https://wokwi.com/projects/470194701675629569

## Six Key Commits

1. [`a19649b`](https://github.com/abijith-123/iot-device-backend-capstone/commit/a19649bdba407ef041899f7638e8f1d6bbc1b533) — created the secured backend foundation, configuration, validation schemas, database models, and reproducible setup.
2. [`fc50510`](https://github.com/abijith-123/iot-device-backend-capstone/commit/fc5051041017fe6643dad85ee8919cac703c248f) — implemented shared HTTP/MQTT ingestion, authenticated API routes, persistence, and configurable alert rules.
3. [`da85e57`](https://github.com/abijith-123/iot-device-backend-capstone/commit/da85e57a5fee8f799b110ac137244162fe7fa349) — added ESP32 telemetry firmware and the consolidated device, MQTT, API, and alert contract.
4. [`0c604a8`](https://github.com/abijith-123/iot-device-backend-capstone/commit/0c604a8736917ff23b29d2435fc9b699874a2163) — added deployment materials, persistent storage configuration, API tests, and GitHub Actions CI.
5. [`a43b24e`](https://github.com/abijith-123/iot-device-backend-capstone/commit/a43b24e66e88f2f2826434fc95cc86fe7e466e8d) — documented the architecture, completion criteria, ownership boundary, and personal walkthrough.
6. [`636f589`](https://github.com/abijith-123/iot-device-backend-capstone/commit/636f5890f995c57f6a47be73501df6f310ba6dc5) — adapted FastAPI, dependencies, and database configuration for Vercel and managed PostgreSQL.

## Verified Production Result — 22 July 2026

I submitted a production telemetry payload containing 38.5°C temperature, 55% humidity, and 650 ppm gas. The secured API returned HTTP `201`, stored reading number 1, and generated two critical alerts: `high_temperature` and `high_gas`.

I then redeployed the backend and queried the data again. The same reading and both alerts remained available, proving that the application used durable Neon PostgreSQL storage rather than temporary serverless storage. The API credential was rotated after testing and remained stored only in the deployment environment.

The Wokwi project also compiled and ran successfully.

## Personal Walkthrough

The completed annotated screenshot walkthrough is submitted as the alternative to a 3–5 minute recording:

https://github.com/abijith-123/iot-device-backend-capstone/tree/main/docs/walkthrough

It shows the original deployment failure, repository evidence, firmware, running Wokwi simulation, production verification PR, ready Vercel deployment, health result, and successful GitHub Actions test.

## Honest Collaboration Statement

The firmware, backend ingestion path, validation, database structure, secured API, alert rules, backend tests, deployment configuration, and related documentation are genuinely my work. Integration required agreement on common JSON fields, authentication headers, filtering options, alert response fields, and deployed endpoint addresses.

I received and provided help while checking the connection between project layers, but I only claim the device and backend implementation supported by my commits, merged pull requests, source code, deployment evidence, and walkthrough.
