# 3–5 Minute Individual Walkthrough

Record one continuous screen capture with your microphone. Keep the GitHub branch and PR visible whenever possible so the demo and authorship evidence reinforce each other.

## 0:00–0:35 — Ownership and architecture

- Open the README architecture diagram.
- Say: “I owned the device and backend path from ESP32 firmware through ingestion, persistence, secured API, and alerts. Seif consumes my API in the dashboard.”
- Trace ESP32 → MQTT → ingestion → database → API → dashboard/alerts.

## 0:35–1:15 — Firmware and protocol

- Open `firmware/esp32_telemetry.ino` on your branch.
- Point out DHT/gas sampling, the five-second interval, reconnect logic, MQTT topic, QoS-compatible broker path, and JSON payload.
- Open `PROTOCOL.md` and match the payload fields to the API contract.

## 1:15–2:30 — Ingestion and alert demo

- Open the deployed `/docs` page.
- Call `POST /api/v1/telemetry` with a correct `X-API-Key` and values such as temperature 38.5 and gas 650.
- Explain that schema validation runs before SQLAlchemy persistence.
- Show the `201` result with both `high_temperature` and `high_gas` alerts.
- Call `GET /api/v1/readings` and `GET /api/v1/alerts?acknowledged=false`.
- Acknowledge one alert and show its state change.

## 2:30–3:15 — Reliability and deployment

- Show the passing GitHub Actions workflow and `tests/test_api.py`.
- Show `Dockerfile`, `render.yaml`, and the live `/health` response.
- Explain environment-based secrets, the persistent disk, and why `/health` is public while telemetry is secured.

## 3:15–4:15 — Evidence and team boundary

- Open the contribution branch and PR.
- Show 4–6 key commit links in `CONTRIBUTION.md`; briefly state what each delivered.
- Show the PR Files changed view.
- End by showing Seif's dashboard receiving the deployed API response, while clearly stating that the dashboard implementation is his contribution.

## Screenshot fallback

If recording is unavailable, capture and annotate these six screenshots: architecture diagram; firmware payload; successful ingestion response; generated alerts; passing CI; branch/PR/commit evidence. Put them in `docs/walkthrough/` and link each image here with a one-sentence explanation.

