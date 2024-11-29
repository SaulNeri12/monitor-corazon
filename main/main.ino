
#include <Arduino.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include <NoDelay.h>
#include <ESPAsyncWebServer.h>
#include <WebSerial.h>

#include "MonitorCorazon.h"

AsyncWebServer server(80);

const char *ssid = "MEGACABLE-46F8";   // Your WiFi SSID
const char *password = "8DYNFNU8BU14"; // Your WiFi Password

IMonitorCorazon *monitorAD8232;

unsigned long last_print_time = millis();

void setup()
{
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  monitorAD8232 = new MonitorStub();

  monitorAD8232->iniciar(0x00);

  while (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
    Serial.printf(".");
    delay(1000);
  }

  // Once connected, print IP
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request)
            { request->send(200, "text/plain", "Hi! This is WebSerial demo. You can access webserial interface at http://" + WiFi.localIP().toString() + "/webserial"); });

  server.on("/bpm", HTTP_GET, [](AsyncWebServerRequest *request)
            { request->send(200, "text/plain", String(monitorAD8232->leerSenialDigital())); });

  // WebSerial is accessible at "<IP Address>/webserial" in browser
  WebSerial.begin(&server);

  /* Attach Message Callback */
  WebSerial.onMessage([&](uint8_t *data, size_t len)
                      {
    Serial.printf("Received %u bytes from WebSerial: ", len);
    Serial.write(data, len);
    Serial.println();
    WebSerial.println("Received Data...");
    String d = "";
    for(size_t i=0; i < len; i++){
      d += char(data[i]);
    }
    WebSerial.println(d); });

  // Start server
  server.begin();
}

void loop()
{
  // Print every 2 seconds (non-blocking)
  if ((unsigned long)(millis() - last_print_time) > 2000)
  {
    WebSerial.print(F("IP address: "));
    WebSerial.println(WiFi.localIP());
    WebSerial.printf("Uptime: %lums\n", millis());
    WebSerial.printf("Free heap: %" PRIu32 "\n", ESP.getFreeHeap());
    last_print_time = millis();
  }

  WebSerial.loop();
}

