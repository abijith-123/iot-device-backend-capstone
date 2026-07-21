# Capstone Learning Note — Abijith Biju

## What “done” means

A real project is done only when it works outside the developer's laptop, another person can reproduce it, and its behavior can be checked. For this platform that means the API has a repeatable container deployment, secrets are configured outside Git, data survives restarts, a health endpoint proves the service is running, automated tests cover ingestion and alerts, and the README gives a new developer one path from clone to working service. “It worked once locally” is a milestone, not completion.

## Architecture communication

A useful architecture diagram gives a stranger the system's shape before they read code. The device-to-MQTT-to-ingestion-to-database-to-API-to-dashboard chain shows both data flow and ownership boundaries. The README then answers the practical questions: what the project does, which technologies it uses, where it is deployed, and how to run or test it. Detailed architecture and protocol documents explain decisions without overcrowding the first page. Together, these reduce onboarding from hours of code reading to minutes of orientation.

## Individual accountability

Branches, commits, and pull requests are the professional record of team work. A branch isolates a contribution, focused commits show the order and intent of changes, and a pull request creates a reviewable discussion around the complete result. This record is stronger than a verbal claim because each link shows the author, timestamp, diff, and context. I should be able to explain every line I claim—from ESP32 reconnection and MQTT topics through validation, storage, API authentication, and alert thresholds—and clearly identify the dashboard and frontend work owned by Seif.

