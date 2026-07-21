# Individual Contribution — Abijith Biju

## Layer owned

I owned the **device and backend chain: ESP32 firmware → MQTT/HTTP ingestion → telemetry persistence → secured API → rule-based alerts**. My boundary ends at the documented REST contract. Seif Taha owns the dashboard, analytics presentation, frontend authentication/integration, and dashboard deployment.

## Evidence

- Repository: https://github.com/abijith-123/iot-device-backend-capstone
- Branch: https://github.com/abijith-123/iot-device-backend-capstone/tree/agent/device-backend-capstone
- Pull request: added after the capstone PR is opened

### Key commits

The final GitHub commit URLs will be inserted here after the five capstone commits are published. Each will map to one defensible unit: service foundation, ingestion/alerts, firmware, verification/deployment, and documentation.

## Personal walkthrough

Use [WALKTHROUGH.md](WALKTHROUGH.md) for a 3–5 minute recording plan and the exact evidence to show. The walkthrough demonstrates the firmware payload, MQTT/HTTP ingestion, persisted reading, generated alerts, acknowledgement, tests, and the handoff to Seif's dashboard contract.

## Honest collaboration statement

The firmware, backend ingestion path, data model, API implementation, alert rules, backend tests, and backend deployment materials in this repository are my contribution. Seif's contribution is the dashboard, analytics UI, frontend authentication/integration, and presentation of the data returned by this API. We collaborate at the boundary: we agree on field names, authentication headers, filtering behavior, alert shape, and deployed URLs; we also test the final device-to-dashboard chain together. Any debugging advice or integration adjustments across that boundary are shared help, but I do not claim Seif's frontend implementation and he should not claim my firmware or backend engine.

