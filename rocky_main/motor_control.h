#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include <Arduino.h>
#include <Servo.h>
#include <map>

#define R1PIN 0
#define R2PIN 13
#define R3PIN 12 

#define L1PIN 0
#define L2PIN 9
#define L3PIN 10

static const int NUM_MOTORS = 6;

extern Servo r1;
extern Servo r2;
extern Servo r3;

extern Servo l1;
extern Servo l2;
extern Servo l3;

extern std::map<String, Servo*> motor_map;

void init_motors();
void turn(String motor, int angle);

#endif