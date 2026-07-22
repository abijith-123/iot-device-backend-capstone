# Week 8 Capstone Final Submission

**Student Name:** Abijith Biju  
**Project:** Device & Backend Capstone — Deploy, Document & Defend Your IoT Platform  
**Repository:** https://github.com/abijith-123/iot-device-backend-capstone  
**Assigned Responsibility:** ESP32 firmware, telemetry ingestion, backend API, database persistence, alert engine, backend deployment, testing, and documentation

---

## Project Overview

This week was the final stage of the IoT capstone. The main goal was not to add more features, but to finish the platform properly. I focused on deploying my device and backend layer, checking that it worked outside my laptop, completing the technical documentation, and collecting clear GitHub evidence for the work I personally completed.

My part of the platform covers the complete path from the ESP32 device to the secured backend API. The device reads temperature, humidity, and simulated gas values. These values are prepared as JSON telemetry and delivered through MQTT or authenticated HTTP. The backend validates the data, stores it in a database, checks the values against alert thresholds, and provides the stored readings and alerts through secured API endpoints.

---

# Part 1 — Learn

## 1. What “Done” Means for a Real Project

Before this capstone, I usually considered a project complete when the code worked on my own computer. During this final week, I understood that this is only one stage of completion. A real project should work outside the developer’s laptop and should not depend on the developer being present every time it is used.

For this project, “done” meant that the backend had to be deployed, the database had to keep information after a redeployment, secrets had to remain outside the public repository, tests had to pass, and another person had to be able to follow the documentation and understand how the system works.

I also learned that deployment is part of development. A project can work correctly in VS Code and still fail in production because the cloud environment handles dependencies, file storage, environment variables, and long-running processes differently. Solving these issues was an important part of completing the platform.

## 2. Communicating the Architecture Clearly

An architecture diagram gives a quick picture of how the main components are connected. In my part of the platform, the data begins at the ESP32 and moves through the following chain:

**ESP32 sensors → JSON telemetry → MQTT or secured HTTP ingestion → validation service → database → alert engine → secured REST API**

The diagram helps a new person understand the flow before reading the code. It also makes it easier to identify where an issue may happen, such as during device connection, message delivery, input validation, database storage, or alert generation.

The README gives the first overview of the project. It explains the purpose, features, technology stack, live links, local setup, testing commands, and deployment steps. The architecture and protocol files provide more technical details without making the first page too crowded.

## 3. Individual Accountability in Team Projects

Branches, commits, and pull requests provide a professional record of each person’s work. A branch separates a piece of work from the main project. Commits show the order in which the work was developed, and pull requests explain what changed, why it changed, and how it was tested.

This evidence is more reliable than only writing a paragraph about my contribution. The GitHub links show the actual author, timestamp, changed files, and technical details. I should also be able to explain every part I claim, including the ESP32 telemetry format, MQTT topics, API authentication, database models, validation rules, alert thresholds, automated tests, and deployment fixes.

My contribution is limited to the device and backend layer shown by my source code and GitHub history. The external dashboard or frontend layer is outside the work claimed in this submission.

---

# Part 2 — Apply

## 1. My Assigned Layer

I owned the complete device-to-backend chain:

**ESP32 firmware → MQTT/HTTP ingestion → telemetry validation → database persistence → secured API → threshold-based alerts**

My work included:

- ESP32 firmware for temperature, humidity, and gas telemetry
- Wi-Fi and MQTT connection handling
- JSON message creation and a five-second publishing interval
- MQTT ingestion and authenticated HTTP ingestion
- Pydantic validation for incoming readings
- SQLAlchemy database models for readings and alerts
- FastAPI endpoints protected with an API key
- Configurable temperature, humidity, and gas alert rules
- Alert acknowledgement support
- Local SQLite storage and production Neon PostgreSQL storage
- Backend tests using Pytest
- GitHub Actions continuous integration
- Vercel deployment configuration
- Architecture, API, setup, and contribution documentation

## 2. ESP32 Firmware

The ESP32 firmware reads temperature and humidity from a DHT22 sensor and reads a simulated gas value from an analog input. Every five seconds, it creates a JSON payload containing the device ID and the three measurements.

The MQTT topic used by the device is:

`iot/esp32-capstone-01/telemetry`

The firmware also prints every JSON payload to the Serial Monitor. This made it possible to verify the device output during simulation even when the public MQTT broker was temporarily unavailable. The completed firmware was compiled and run using Wokwi.

**Live Wokwi simulation:**  
https://wokwi.com/projects/470194701675629569

## 3. Ingestion, Validation, and Security

The backend supports two telemetry entry methods. MQTT is used for the IoT message path, while the HTTP endpoint can be used for production delivery, testing, broker webhooks, or a direct device connection.

Both paths use the same validation and ingestion service. This prevents the system from having different storage or alert behavior depending on how the message arrived.

Pydantic checks the incoming fields before the data is stored. It rejects invalid device IDs, impossible sensor ranges, malformed JSON, and unsuitable timestamps.

Every `/api/v1/*` endpoint requires the `X-API-Key` header. The production key is stored only in Vercel environment variables and is not included in the GitHub repository. The public health endpoint only confirms that the service is running and does not reveal private telemetry data.

## 4. Database and Alert Engine

SQLAlchemy is used for the database layer. SQLite supports local development and automated testing, while Neon PostgreSQL provides permanent storage for the deployed Vercel backend.

The alert engine checks every valid reading against three configurable rules:

| Alert Rule | Default Trigger | Severity |
|---|---:|---|
| High temperature | Temperature greater than 35°C | Critical |
| High humidity | Humidity greater than 80% | Warning |
| High gas | Gas value greater than 500 ppm | Critical |

One reading can generate more than one alert. Each alert records the device, related reading, measured value, threshold, severity, message, time, and acknowledgement state.

The reading and its related alerts are created through the same ingestion process. This helps prevent a reading from being stored without its required alerts.

## 5. Backend API

The backend provides the following endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Public deployment health check |
| POST | `/api/v1/telemetry` | Store a reading and evaluate alert rules |
| GET | `/api/v1/readings` | Return stored readings with optional filtering |
| GET | `/api/v1/alerts` | Return alerts with optional filtering |
| PATCH | `/api/v1/alerts/{alert_id}/acknowledge` | Mark an alert as acknowledged |

**Live backend health:**  
https://iot-device-backend-capstone.vercel.app/health

**Interactive API documentation:**  
https://iot-device-backend-capstone.vercel.app/docs

## 6. Deployment Problems and Fixes

The backend worked locally, but I faced important issues when deploying it to Vercel.

The first issue happened because the required Python packages were not being installed from the original project configuration. This caused the deployed function to fail while importing FastAPI. I corrected the production dependency configuration and redeployed the project.

The second issue happened because the serverless deployment tried to create a SQLite database inside a read-only application directory. I added a safe temporary fallback for Vercel and connected Neon PostgreSQL as the permanent production storage solution.

I also learned that a Vercel function cannot remain connected to an MQTT broker as a permanent background subscriber. For production, telemetry should reach the secured HTTP endpoint directly or through a broker webhook or rule. The included MQTT worker can still run in a local or container deployment.

## 7. Final Production Verification

On 22 July 2026, I tested the deployed backend using a telemetry reading that crossed more than one threshold.

The submitted values were:

- Temperature: `38.5°C`
- Humidity: `55%`
- Gas concentration: `650 ppm`

The production API returned HTTP status `201`, stored reading number 1, and generated two critical alerts:

- `high_temperature`, because `38.5°C` was greater than the `35°C` threshold
- `high_gas`, because `650 ppm` was greater than the `500 ppm` threshold

After this test, I redeployed the production backend and queried the readings and alerts again. The same reading and both alerts were still available. This proved that the deployed application was using permanent Neon PostgreSQL storage rather than temporary serverless storage.

The production API key was rotated after the verification and remained stored only in Vercel environment variables.

## 8. Documentation Completed

The repository contains the following final documentation:

- `README.md` — overview, features, live links, setup, tests, and deployment
- `CAPSTONE.md` — learning note about completion, architecture, and accountability
- `ARCHITECTURE.md` — backend components, data flow, security, and reliability
- `PROTOCOL.md` — MQTT format, API endpoints, authentication, errors, and alerts
- `CONTRIBUTION.md` — my ownership, evidence links, commits, and honest statement
- `docs/walkthrough/README.md` — annotated personal walkthrough evidence
- `SUBMISSION.md` — final submission index
- `WEEK8_SUBMISSION.md` — complete Week 8 written report

---

# Individual Contribution Showcase

## 1. Contribution Statement

I personally developed the ESP32 firmware, telemetry message format, MQTT and HTTP ingestion, validation schemas, database models, persistence service, secured FastAPI routes, rule-based alert engine, backend tests, Vercel deployment configuration, and backend documentation.

The external dashboard and frontend implementation are not claimed in this submission. Collaboration was limited to agreeing on the data and API boundary required for integration.

## 2. Main Evidence Links

**Repository:**  
https://github.com/abijith-123/iot-device-backend-capstone

**Main contribution branch:**  
https://github.com/abijith-123/iot-device-backend-capstone/tree/agent/device-backend-capstone

**Main implementation pull request:**  
https://github.com/abijith-123/iot-device-backend-capstone/pull/1

**Vercel deployment adaptation:**  
https://github.com/abijith-123/iot-device-backend-capstone/pull/2

**Dependency correction:**  
https://github.com/abijith-123/iot-device-backend-capstone/pull/3

**Serverless storage correction:**  
https://github.com/abijith-123/iot-device-backend-capstone/pull/4

**Verified Vercel deployment evidence:**  
https://github.com/abijith-123/iot-device-backend-capstone/pull/5

**Neon production persistence verification:**  
https://github.com/abijith-123/iot-device-backend-capstone/pull/6

**Final simulator and walkthrough evidence:**  
https://github.com/abijith-123/iot-device-backend-capstone/pull/8

**Passing backend CI evidence:**  
https://github.com/abijith-123/iot-device-backend-capstone/pull/9

## 3. Six Key Commits

1. **Backend foundation**  
   https://github.com/abijith-123/iot-device-backend-capstone/commit/a19649bdba407ef041899f7638e8f1d6bbc1b533  
   Created the secured backend structure, configuration, validation schemas, database models, and reproducible setup.

2. **Ingestion, API, persistence, and alerts**  
   https://github.com/abijith-123/iot-device-backend-capstone/commit/fc5051041017fe6643dad85ee8919cac703c248f  
   Implemented the shared HTTP/MQTT ingestion process, authenticated routes, database persistence, and configurable alert evaluation.

3. **ESP32 firmware and protocol**  
   https://github.com/abijith-123/iot-device-backend-capstone/commit/da85e57a5fee8f799b110ac137244162fe7fa349  
   Added the ESP32 firmware and documented the agreed telemetry, MQTT, API, and alert contract.

4. **Deployment, tests, and CI**  
   https://github.com/abijith-123/iot-device-backend-capstone/commit/0c604a8736917ff23b29d2435fc9b699874a2163  
   Added Docker and cloud deployment materials, backend tests, persistent storage configuration, and GitHub Actions.

5. **Architecture and individual evidence**  
   https://github.com/abijith-123/iot-device-backend-capstone/commit/a43b24e66e88f2f2826434fc95cc86fe7e466e8d  
   Documented the architecture, ownership boundary, completion criteria, and personal walkthrough.

6. **Vercel and managed PostgreSQL adaptation**  
   https://github.com/abijith-123/iot-device-backend-capstone/commit/636f5890f995c57f6a47be73501df6f310ba6dc5  
   Adapted the FastAPI entry point, dependencies, database configuration, and deployment instructions for Vercel.

## 4. Personal Walkthrough

I submitted an annotated screenshot walkthrough as the alternative to a 3–5 minute screen recording.

The walkthrough shows:

1. The original Vercel deployment failure
2. The GitHub repository and ownership record
3. The ESP32 firmware and telemetry structure
4. The running Wokwi simulator
5. The merged database verification pull request
6. The ready Vercel production deployment
7. The public health response
8. The successful GitHub Actions backend test

**Walkthrough:**  
https://github.com/abijith-123/iot-device-backend-capstone/tree/main/docs/walkthrough

## 5. Honest Collaboration Statement

The firmware, backend ingestion path, validation, database structure, secured API, alert rules, tests, backend deployment, and related documentation are genuinely my work. Integration required agreement on common JSON fields, authentication headers, query options, alert response fields, and deployed endpoint addresses.

I received and provided help while checking the connection between project layers, but I only claim the device and backend implementation supported by my branch, commits, pull requests, source code, deployment evidence, and walkthrough.

---

# Final Reflection

This final week helped me understand the difference between building a feature and delivering a complete project. The most valuable part for me was solving the deployment problems because they showed that cloud environments behave differently from local development.

I also improved my understanding of API security, environment variables, database persistence, serverless limitations, automated testing, and professional GitHub evidence. The project is now easier for another developer to understand, run, test, and verify.

I am more confident in explaining the complete device-to-backend flow and defending the work I personally completed. At the same time, I understand that a larger production system would need stronger device-level authentication, broker TLS, message deduplication, monitoring, and a dedicated long-running MQTT consumer.