# Individual Contribution — Abijith Biju

## Layer owned

I owned the **device and backend chain: ESP32 firmware → MQTT/HTTP ingestion → telemetry persistence → secured API → rule-based alerts**. My boundary ends at the documented REST contract. Seif Taha owns the dashboard, analytics presentation, frontend authentication/integration, and dashboard deployment.

## Evidence

- Repository: https://github.com/abijith-123/iot-device-backend-capstone
- Branch: https://github.com/abijith-123/iot-device-backend-capstone/tree/agent/device-backend-capstone
- Pull request: https://github.com/abijith-123/iot-device-backend-capstone/pull/1
- Live backend health: https://iot-device-backend-capstone.vercel.app/health
- Live interactive API documentation: https://iot-device-backend-capstone.vercel.app/docs
- Vercel adaptation PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/2
- Vercel dependency fix PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/3
- Vercel runtime-storage fix PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/4
- Verified Vercel deployment evidence PR: https://github.com/abijith-123/iot-device-backend-capstone/pull/5
- Production verification branch: https://github.com/abijith-123/iot-device-backend-capstone/tree/agent/verify-neon-production
- Durable production database: Neon PostgreSQL connected through Vercel

### Key commits

- [`a19649b`](https://github.com/abijith-123/iot-device-backend-capstone/commit/a19649bdba407ef041899f7638e8f1d6bbc1b533) — built the secured telemetry service foundation, configuration, validation schemas, database model, and reproducible project setup.
- [`fc50510`](https://github.com/abijith-123/iot-device-backend-capstone/commit/fc5051041017fe6643dad85ee8919cac703c248f) — implemented shared HTTP/MQTT ingestion, authenticated API routes, persistence, and configurable multi-rule alerts.
- [`da85e57`](https://github.com/abijith-123/iot-device-backend-capstone/commit/da85e57a5fee8f799b110ac137244162fe7fa349) — added ESP32 telemetry firmware plus the consolidated device, MQTT, API, and alert contract.
- [`0c604a8`](https://github.com/abijith-123/iot-device-backend-capstone/commit/0c604a8736917ff23b29d2435fc9b699874a2163) — added Docker/Render deployment, persistent storage configuration, automated API tests, and GitHub Actions CI.
- [`a43b24e`](https://github.com/abijith-123/iot-device-backend-capstone/commit/a43b24e66e88f2f2826434fc95cc86fe7e466e8d) — documented backend architecture, completion criteria, ownership boundaries, and the personal walkthrough.
- [`636f589`](https://github.com/abijith-123/iot-device-backend-capstone/commit/636f5890f995c57f6a47be73501df6f310ba6dc5) — adapted the FastAPI entry point, database configuration, and deployment documentation for Vercel and managed PostgreSQL.

## Verified production result — 22 July 2026

I sent a threshold-breaching payload through the secured production endpoint. The API returned **201**, stored reading **#1**, and produced two critical alerts: `high_temperature` for `38.5°C > 35°C` and `high_gas` for `650 ppm > 500 ppm`. I then rotated the API credential, redeployed production, and queried the service again. The same reading and both alerts remained available, proving that the deployed API uses durable Neon PostgreSQL rather than temporary serverless storage.

Seif's dashboard is treated as **ready for integration for planning purposes**, but I have not marked it deployed or end-to-end verified. That status requires Seif's live dashboard URL and his own commit/PR/walkthrough evidence.

## Personal walkthrough

Use [WALKTHROUGH.md](WALKTHROUGH.md) for a 3–5 minute recording plan and the exact evidence to show. The walkthrough demonstrates the firmware payload, MQTT/HTTP ingestion, persisted reading, generated alerts, acknowledgement, tests, and the handoff to Seif's dashboard contract.

## Honest collaboration statement

The firmware, backend ingestion path, data model, API implementation, alert rules, backend tests, and Vercel deployment materials in this repository are my contribution. Seif's contribution is the dashboard, analytics UI, frontend authentication/integration, and presentation of the data returned by this API. We collaborate at the boundary: we agree on field names, authentication headers, filtering behavior, alert shape, and deployed URLs; we also test the final device-to-dashboard chain together. Any debugging advice or integration adjustments across that boundary are shared help, but I do not claim Seif's frontend implementation and he should not claim my firmware or backend engine.
