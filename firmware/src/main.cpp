#include <Arduino.h>
#include <HID.h>
#include <Mouse.h>

void setup() {
  Serial.begin(115200);
  Serial.print("[success] Init serial\n");
  Mouse.begin();
  Serial.print("[success] Init mouse\n");
}

void loop() {
  if (Serial.available() >= 2) {
    int8_t dx = (int8_t)Serial.read();
    int8_t dy = (int8_t)Serial.read();

    Mouse.move(dx, dy, 0);
  }
}