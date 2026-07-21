# Wokwi ESP32 Simulation

This folder contains everything needed to reproduce the device simulation:

- `esp32_telemetry.ino` — firmware that samples the DHT22 and gas input and publishes JSON telemetry.
- `diagram.json` — ESP32, DHT22, and potentiometer circuit. The potentiometer emulates the analog gas sensor.
- `libraries.txt` — Wokwi library dependencies.

## Run in Wokwi

1. Create an ESP32 project at https://wokwi.com/projects/new/esp32.
2. Replace `sketch.ino` with the contents of `esp32_telemetry.ino`.
3. Replace `diagram.json` with this folder's `diagram.json`.
4. Add the libraries listed in `libraries.txt`.
5. Start the simulation and open the Serial Monitor.
6. Change the DHT22 values or turn the potentiometer to demonstrate changing telemetry.

The public simulation publishes to `iot/esp32-capstone-01/telemetry` on the HiveMQ public broker. The local/container backend can subscribe with `MQTT_ENABLED=true`. Vercel cannot keep a permanent MQTT subscription, so the verified serverless path uses the same JSON contract through secured HTTP ingestion or an MQTT broker rule/webhook.

Never place the production `API_KEY` in a public Wokwi project.
