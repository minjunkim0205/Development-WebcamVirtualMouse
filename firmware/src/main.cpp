#include <Arduino.h>
#include <Mouse.h>

#define CMD_MOVE          0x01
#define CMD_LEFT_CLICK    0x02
#define CMD_RIGHT_CLICK   0x03
#define CMD_MIDDLE_CLICK  0x04
#define CMD_LEFT_PRESS    0x05
#define CMD_LEFT_RELEASE  0x06
#define CMD_RIGHT_PRESS   0x07
#define CMD_RIGHT_RELEASE 0x08
#define CMD_SCROLL        0x09

bool readByteWithTimeout(int8_t &value, unsigned long timeoutMs = 20) {
  unsigned long start = millis();

  while (Serial.available() < 1) {
    if (millis() - start > timeoutMs) {
      return false;
    }
  }

  value = (int8_t)Serial.read();
  return true;
}

void setup() {
  Serial.begin(115200);
  Mouse.begin();
}

void loop() {
  if (Serial.available() < 1) {
    return;
  }

  uint8_t cmd = Serial.read();

  switch (cmd) {
    case CMD_MOVE: {
      int8_t dx, dy;

      if (!readByteWithTimeout(dx)) return;
      if (!readByteWithTimeout(dy)) return;

      Mouse.move(dx, dy, 0);
      break;
    }

    case CMD_LEFT_CLICK:
      Mouse.click(MOUSE_LEFT);
      break;

    case CMD_RIGHT_CLICK:
      Mouse.click(MOUSE_RIGHT);
      break;

    case CMD_MIDDLE_CLICK:
      Mouse.click(MOUSE_MIDDLE);
      break;

    case CMD_LEFT_PRESS:
      Mouse.press(MOUSE_LEFT);
      break;

    case CMD_LEFT_RELEASE:
      Mouse.release(MOUSE_LEFT);
      break;

    case CMD_RIGHT_PRESS:
      Mouse.press(MOUSE_RIGHT);
      break;

    case CMD_RIGHT_RELEASE:
      Mouse.release(MOUSE_RIGHT);
      break;

    case CMD_SCROLL: {
      int8_t amount;

      if (!readByteWithTimeout(amount)) return;

      Mouse.move(0, 0, amount);
      break;
    }
  }
}