#include <Arduino.h>
#include <Servo.h>

#include "motor_control.h"

String motors[NUM_MOTORS] = {
  "r1", "r2", "r3", "l1", "l2", "l3"
};

int angles[NUM_MOTORS];

void setup() {
  Serial.begin(115200);
  init_motors();

  r2.write(150);
  r3.write(150);
  l2.write(30);
  l3.write(30);
  
}

bool parsePacket(String line) {
  int start = 0;
  int idx = 0;

  for (int i = 0; i < NUM_MOTORS; i++) {
    int commaIndex = line.indexOf(',', start);

    if (commaIndex == -1 && i < NUM_MOTORS - 1) return false;

    String token;
    if (i == NUM_MOTORS - 1) {
      token = line.substring(start);
    } else {
      token = line.substring(start, commaIndex);
    }

    angles[i] = token.toInt();
    start = commaIndex + 1;
  }

  return true;
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (parsePacket(line)) {
      for (int i = 0; i < NUM_MOTORS; i++) {
        turn(motors[i], angles[i]);
      }
    }
  }
}