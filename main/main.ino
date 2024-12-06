
#include <Arduino.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include <NoDelay.h>
#include <ESPAsyncWebServer.h>
#include <WebSerial.h>

#include "FS.h"
#include "LittleFS.h"

AsyncWebServer server(80);

const char *ssid = "CHURRUMAIS";    // Your WiFi SSID
const char *password = "12345678";  // Your WiFi Password

// Pin definitions
#define ECG_PIN 34
#define LO_POS 32
#define LO_NEG 33
#define LED_PIN 2
#define BUZZER_PIN 27

// Sampling and analysis constants
#define SAMPLE_SIZE 30      // Reduced from 50 to 30 for faster processing
#define BASE_LINE 2048      // Baseline for 12-bit ADC
#define SAMPLE_INTERVAL 5   // Reduced from 10ms to 5ms
#define PRINT_INTERVAL 500  // Reduced from 1000ms to 500ms
#define THRESHOLD_FACTOR 1.2
#define MIN_PEAK_DISTANCE 100  // Reduced from 200ms to 100ms

// Critical BPM ranges
const int CRITICAL_HIGH_BPM = 120;
const int CRITICAL_LOW_BPM = 50;
const int WARNING_INTERVAL = 1000;  // Reduced from 2000ms to 1000ms

class HeartRateMonitor {
private:
  int samples[SAMPLE_SIZE];
  int sampleIndex = 0;
  int lastPeakValue = 0;

  unsigned long lastPeakTime = 0;
  unsigned long lastPrintTime = 0;
  unsigned long lastSampleTime = 0;
  unsigned long lastWarningTime = 0;

  int bpm = 0;
  float avgBpm = 0;
  const float ALPHA = 0.15;  // Increased from 0.1 for faster response

  bool leadsConnected = false;
  bool isPeak = false;
  bool isWarning = false;

  const int PATTERN_HIGH[4] = { 1000, 100, 1000, 100 };  // Faster pattern
  const int PATTERN_LOW[4] = { 500, 250, 500, 250 };     // Faster pattern

public:
  void begin() {
    pinMode(ECG_PIN, INPUT);
    pinMode(LO_POS, INPUT);
    pinMode(LO_NEG, INPUT);
    pinMode(LED_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);

    for (int i = 0; i < SAMPLE_SIZE; i++) {
      samples[i] = BASE_LINE;
    }
  }

  int getBPM() {
    return bpm;
  }

  int getECG() {
    return analogRead(ECG_PIN);
  }

  void update() {
    unsigned long currentTime = millis();

    leadsConnected = (digitalRead(LO_POS) == 0) && (digitalRead(LO_NEG) == 0);

    if (currentTime - lastSampleTime >= SAMPLE_INTERVAL) {
      updateSamples();
      checkBPMStatus(currentTime);
      lastSampleTime = currentTime;
    }

    if (currentTime - lastPrintTime >= PRINT_INTERVAL) {
      printData();
      lastPrintTime = currentTime;
    }
  }

private:
  void checkBPMStatus(unsigned long currentTime) {
    if (!leadsConnected || bpm == 0) {
      stopBuzzer();
      return;
    }

    if (currentTime - lastWarningTime < WARNING_INTERVAL) {
      return;
    }

    if (bpm >= CRITICAL_HIGH_BPM) {
      playWarning(true);
      lastWarningTime = currentTime;
      isWarning = true;
    } else if (bpm <= CRITICAL_LOW_BPM) {
      playWarning(false);
      lastWarningTime = currentTime;
      isWarning = true;
    } else {
      stopBuzzer();
      isWarning = false;
    }
  }

  void playWarning(bool isHighBPM) {
    const int *pattern = isHighBPM ? PATTERN_HIGH : PATTERN_LOW;

    tone(BUZZER_PIN, pattern[0], pattern[1]);
    delay(pattern[1]);
    noTone(BUZZER_PIN);
    delay(25);  // Reduced delay
    tone(BUZZER_PIN, pattern[2], pattern[3]);
    delay(pattern[3]);
    noTone(BUZZER_PIN);
  }

  void stopBuzzer() {
    noTone(BUZZER_PIN);
  }

  void updateSamples() {
    if (!leadsConnected) return;

    int rawValue = analogRead(ECG_PIN);

    if (rawValue >= 4000 || rawValue <= 100) return;

    samples[sampleIndex] = rawValue;
    sampleIndex = (sampleIndex + 1) % SAMPLE_SIZE;

    detectPeak(rawValue);
  }

  void detectPeak(int currentValue) {
    unsigned long currentTime = millis();

    int sum = 0;
    for (int i = 0; i < SAMPLE_SIZE; i++) {
      sum += samples[i];
    }
    int average = sum / SAMPLE_SIZE;

    if (currentValue > average * THRESHOLD_FACTOR && currentValue > lastPeakValue && (currentTime - lastPeakTime) > MIN_PEAK_DISTANCE) {

      if (lastPeakTime != 0) {
        int interval = currentTime - lastPeakTime;
        int newBpm = 60000 / interval;

        if (newBpm >= 40 && newBpm <= 200) {
          if (avgBpm == 0) avgBpm = newBpm;
          else avgBpm = (ALPHA * newBpm) + ((1 - ALPHA) * avgBpm);

          bpm = round(avgBpm);

          digitalWrite(LED_PIN, HIGH);
          delay(25);  // Reduced LED flash time
          digitalWrite(LED_PIN, LOW);
        }
      }

      lastPeakTime = currentTime;
      lastPeakValue = currentValue;
      isPeak = true;
    } else {
      isPeak = false;
      if (currentTime - lastPeakTime > 1000) {  // Reduced from 2000ms to 1000ms
        lastPeakValue = 0;
      }
    }
  }

  void printData() {
    Serial.print("ECG:");
    Serial.print(analogRead(ECG_PIN));
    Serial.print(",BPM:");
    Serial.print(bpm);
    Serial.print(",Pico:");
    Serial.print(isPeak ? 4000 : 1000);
    Serial.print(",Alerta:");
    Serial.println(isWarning ? 3000 : 1000);
  }
};


unsigned long last_print_time = millis();

HeartRateMonitor heartMonitor;

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  heartMonitor.begin();

  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.printf(".");
    delay(1000);
  }

  // Once connected, print IP
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/plain", "Hi! This is WebSerial demo. You can access webserial interface at http://" + WiFi.localIP().toString() + "/webserial");
  });

  server.on("/monitor", HTTP_GET, [](AsyncWebServerRequest *request) {
    File file = LittleFS.open("/pagina.html", "r");  // Abrir el archivo en modo lectura

    if (!file) {
      request->send(404, "text/plain", "Archivo no encontrado");
      return;
    }


    String content = file.readString();  // Leer todo el contenido del archivo
    
    AsyncWebServerResponse *response = request->beginResponse(200, "text/html", content);
    request->send(response);

    file.close();
  });

  server.on("/bpm", HTTP_GET, [](AsyncWebServerRequest *request) {
    AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", String(heartMonitor.getBPM()));
    response->addHeader("Access-Control-Allow-Origin", "*");
    response->addHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    response->addHeader("Access-Control-Allow-Headers", "Content-Type");
    request->send(response);
  });

  server.on("/ecg", HTTP_GET, [](AsyncWebServerRequest *request) {
    AsyncWebServerResponse *response = request->beginResponse(200, "text/plain", String(heartMonitor.getECG()));
    response->addHeader("Access-Control-Allow-Origin", "*");
    response->addHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    response->addHeader("Access-Control-Allow-Headers", "Content-Type");
    request->send(response);
  });

  // WebSerial is accessible at "<IP Address>/webserial" in browser
  WebSerial.begin(&server);

  /* Attach Message Callback */
  WebSerial.onMessage([&](uint8_t *data, size_t len) {
    Serial.printf("Received %u bytes from WebSerial: ", len);
    Serial.write(data, len);
    Serial.println();
    WebSerial.println("Received Data...");
    String d = "";
    for (size_t i = 0; i < len; i++) {
      d += char(data[i]);
    }
    WebSerial.println(d);
  });

  // Start server
  server.begin();
}

void loop() {
  // Print every 2 secods (non-blocking)
  heartMonitor.update();
  if ((unsigned long)(millis() - last_print_time) > 2000) {
    WebSerial.print(F("IP address: "));
    WebSerial.println(WiFi.localIP());
    WebSerial.printf("Uptime: %lums\n", millis());
    WebSerial.printf("Free heap: %" PRIu32 "\n", ESP.getFreeHeap());
    last_print_time = millis();
  }

  WebSerial.loop();
}
