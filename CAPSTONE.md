# Capstone Learning Note — Abijith Biju

## What “Done” Means for a Real Project

Before completing this capstone, I normally considered a project finished when the code worked successfully on my laptop. This final week helped me understand that working locally is only one stage of completing a real project.

A proper project should be deployed so that it can run without depending on the developer’s computer. It should also be documented clearly, tested properly, secured, and easy for another person to reproduce. Someone new should be able to open the repository, understand the purpose of the system, follow the setup instructions, and run it without needing the original developer beside them.

For my device and backend platform, being “done” meant deploying the FastAPI service, connecting it to a durable PostgreSQL database, protecting the API using an environment-based API key, and confirming that telemetry and alerts remained available after redeployment. It also meant adding a health endpoint, automated tests, GitHub Actions, clear local setup instructions, and evidence showing that the ESP32 simulation and backend were working.

The project was not complete just because one telemetry request worked. I needed to prove that the data was validated, stored, checked against alert thresholds, and available again through the secured API.

## Communicating the Architecture

A good architecture diagram helps a person understand the overall system before reading individual source-code files. In this project, the main data path starts from the ESP32 sensors. The device prepares a JSON telemetry message and sends it through MQTT or authenticated HTTP. The FastAPI backend validates the message, stores it in the database, checks the values against the configured alert rules, and exposes the readings and alerts through secured API endpoints.

The diagram makes the responsibilities of each component easier to understand. It also shows where a problem could happen, such as at the device connection, message delivery, API validation, database storage, or alert-processing stage.

The README gives a new developer the first overview of the project. It explains the features, technology stack, deployment links, local setup, testing commands, and important security instructions. More detailed documents explain the architecture and the API contract without making the README too crowded.

Together, the README and architecture diagram allow someone to understand the system in a few minutes instead of searching through every folder without guidance.

## Individual Accountability in Teamwork

This project also taught me why branches, commits, and pull requests are important in team development. They are not only GitHub features; they are a professional record of how the project was built.

My branch shows the area of the project I worked on. My commits divide the work into understandable stages, while the pull requests show the complete changes, reasons, testing results, and deployment fixes. This provides stronger evidence than simply saying that I completed the backend.

I should also be able to explain and defend every part that I claim. For my contribution, this includes the ESP32 telemetry format, MQTT topic structure, HTTP ingestion, input validation, API-key security, database models, alert thresholds, testing, and deployment process.

My contribution is limited to the device and backend layer shown by my source code and GitHub history. The external dashboard or frontend layer is outside the work claimed in this submission.