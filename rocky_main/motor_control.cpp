#include <Arduino.h>

#include "motor_control.h"

Servo r1;
Servo r2;
Servo r3;

Servo l1;
Servo l2;
Servo l3;

std::map<String, Servo*> motor_map = {
    {"r1", &r1},
    {"r2", &r2},
    {"r3", &r3},
    {"l1", &l1},
    {"l2", &l2},
    {"l3", &l3},
};

void init_motors() {
  Serial.println("Initializing Motors");
  r1.attach(R1PIN);
  r2.attach(R2PIN);
  r3.attach(R3PIN);

  l1.attach(L1PIN);
  l2.attach(L2PIN);
  l3.attach(L3PIN);
}

void turn(String motor, int angle) {
  auto it = motor_map.find(motor);

    if (it != motor_map.end()) {
        it->second->write(angle);
    } else {
        Serial.println("Unknown motor");
    }
}