
#include <NoDelay.h>
#include "MonitorCorazon.h"

unsigned long previousMillis = 0;
const long interval = 1000;

IMonitorCorazon *monitor;

void setup() {
  Serial.begin(115200);

  monitor = new MonitorStub();

  monitor->iniciar(0x00);

  //pinMode(LED_PIN, OUTPUT);
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    
    Serial.printf("BPM: %d\n", monitor->leerSenialDigital());

    previousMillis = currentMillis;
    //digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
}
