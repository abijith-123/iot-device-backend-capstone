# Final Capstone Submission — Device & Backend

**Student:** Abijith Biju  
**Repository:** https://github.com/abijith-123/iot-device-backend-capstone  
**Submission status:** Ready for assessment

## Live Platform

| Deliverable | Final Link | Verification |
|---|---|---|
| Backend health | https://iot-device-backend-capstone.vercel.app/health | Live production response |
| Interactive API documentation | https://iot-device-backend-capstone.vercel.app/docs | Live FastAPI/OpenAPI contract |
| ESP32 simulator | https://wokwi.com/projects/470194701675629569 | Public project; compiled and running |
| Production database | Neon PostgreSQL through Vercel | Persistence verified across redeployment |

## Required Documents

- [Week 8 written submission](WEEK8_SUBMISSION.md) — complete learning, application, evidence, verification, and reflection report.
- [Top-level project README](README.md) — features, architecture chain, technology stack, live links, local run, tests, and deployment.
- [CAPSTONE.md](CAPSTONE.md) — learning note about project completion, architecture communication, and professional accountability.
- [ARCHITECTURE.md](ARCHITECTURE.md) — backend components, data model, security, reliability, and deployment boundary.
- [PROTOCOL.md](PROTOCOL.md) — MQTT payload, secured endpoints, authentication, errors, and alert contract.
- [CONTRIBUTION.md](CONTRIBUTION.md) — personal ownership, branch and PR links, six key commits, production result, and honest collaboration statement.
- [Annotated screenshot walkthrough](docs/walkthrough/README.md) — completed personal walkthrough evidence.

## Verified End-to-End Backend Result

On 22 July 2026, the production API accepted threshold-breaching telemetry with HTTP **201**, stored reading number 1, and generated `high_temperature` and `high_gas` critical alerts. The same reading and alerts remained available after a fresh deployment, verifying durable PostgreSQL persistence. GitHub Actions also completed the backend test workflow successfully.

## Professional Evidence Record

- Core device and backend implementation: [PR #1](https://github.com/abijith-123/iot-device-backend-capstone/pull/1)
- Vercel and managed-database adaptation: [PRs #2–#6](https://github.com/abijith-123/iot-device-backend-capstone/pulls?q=is%3Apr+is%3Aclosed)
- Final simulator and annotated walkthrough: [PR #8](https://github.com/abijith-123/iot-device-backend-capstone/pull/8)
- Passing CI evidence: [PR #9](https://github.com/abijith-123/iot-device-backend-capstone/pull/9)

## Ownership Declaration

I own the ESP32 firmware, MQTT and HTTP ingestion, input validation, database persistence, secured backend API, rule-based alert engine, backend testing, Vercel deployment materials, and related documentation. My claimed contribution ends at the documented API and integration contract. The external dashboard and frontend implementation are outside this individual submission.

This submission contains final links, completed documents, verified evidence, and no committed secrets.