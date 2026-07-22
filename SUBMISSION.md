# Final Capstone Submission — Device & Backend

**Student:** Abijith Biju  
**Repository:** https://github.com/abijith-123/iot-device-backend-capstone  
**Submission status:** Ready for assessment

## Live platform

| Deliverable | Final link | Verification |
|---|---|---|
| Backend health | https://iot-device-backend-capstone.vercel.app/health | Live production response |
| Interactive API documentation | https://iot-device-backend-capstone.vercel.app/docs | Live FastAPI/OpenAPI contract |
| ESP32 simulator | https://wokwi.com/projects/470194701675629569 | Public project; compiled, started, and connected |
| Production database | Neon PostgreSQL through Vercel | Persistence verified across redeployment |
| Dashboard and analytics | Seif Taha's individual frontend submission | Complete under the team's final declaration |

## Required documents

- [Top-level project README](README.md) — features, architecture chain, stack, live links, local run, tests, and deployment.
- [CAPSTONE.md](CAPSTONE.md) — completion, architecture communication, and professional accountability learning note.
- [ARCHITECTURE.md](ARCHITECTURE.md) — backend components, data model, security, reliability, and deployment boundary.
- [PROTOCOL.md](PROTOCOL.md) — MQTT payload, secured endpoints, authentication, errors, and alert contract.
- [CONTRIBUTION.md](CONTRIBUTION.md) — personal ownership, branch/PR links, six key commits, production result, and honest collaboration statement.
- [Annotated screenshot walkthrough](docs/walkthrough/README.md) — completed personal walkthrough evidence.

## Verified end-to-end backend result

On 22 July 2026, the production API accepted threshold-breaching telemetry with HTTP **201**, stored reading **#1**, and generated `high_temperature` and `high_gas` critical alerts. The same reading and alerts remained available after a fresh deployment, verifying durable PostgreSQL persistence. GitHub Actions also completed the backend test workflow successfully.

## Professional evidence record

- Core device/backend implementation: [PR #1](https://github.com/abijith-123/iot-device-backend-capstone/pull/1)
- Vercel and managed-database adaptation: [PRs #2–#6](https://github.com/abijith-123/iot-device-backend-capstone/pulls?q=is%3Apr+is%3Aclosed)
- Final simulator and annotated walkthrough: [PR #8](https://github.com/abijith-123/iot-device-backend-capstone/pull/8)
- Captured passing CI evidence: [PR #9](https://github.com/abijith-123/iot-device-backend-capstone/pull/9)

## Ownership declaration

Abijith Biju owns the ESP32 firmware, MQTT/HTTP ingestion, persistence, secured backend API, rule-based alert engine, backend testing, and Vercel deployment materials. Seif Taha owns the dashboard, analytics presentation, frontend authentication/integration, and frontend deployment. Shared work is limited to the JSON/API boundary, deployed integration contract, and end-to-end verification.

This submission contains final links, finished documents, verified evidence, and no committed secrets.
