#include <DHTesp.h>
#include <PubSubClient.h>
#include <WiFi.h>

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";
const char* MQTT_HOST = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char* DEVICE_ID = "esp32-capstone-01";
const char* MQTT_TOPIC = "iot/esp32-capstone-01/telemetry";

const int DHT_PIN = 15;
const int GAS_PIN = 34;
const unsigned long PUBLISH_INTERVAL_MS = 5000;

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
DHTesp dht;
unsigned long lastPublish = 0;

void connectWifi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
  }
}

bool connectMqtt() {
  if (mqtt.connected()) return true;
  String clientId = String(DEVICE_ID) + "-" + String(random(0xffff), HEX);
  return mqtt.connect(clientId.c_str());
}

void setup() {
  Serial.begin(115200);
  dht.setup(DHT_PIN, DHTesp::DHT22);
  connectWifi();
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWifi();
  bool mqttReady = mqtt.connected();
  if (mqttReady) mqtt.loop();

  if (millis() - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = millis();
    TempAndHumidity sample = dht.getTempAndHumidity();
    float gasPpm = analogRead(GAS_PIN) * (1000.0 / 4095.0);

    char payload[220];
    snprintf(payload, sizeof(payload),
      "{\"device_id\":\"%s\",\"temperature_c\":%.2f,\"humidity_pct\":%.2f,\"gas_ppm\":%.2f}",
      DEVICE_ID, sample.temperature, sample.humidity, gasPpm);

    Serial.println(payload);
    if (mqttReady) {
      mqtt.publish(MQTT_TOPIC, payload, true);
    } else {
      connectMqtt();
    }
  }
}

