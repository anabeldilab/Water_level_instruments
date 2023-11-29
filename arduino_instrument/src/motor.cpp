#include "..\include\motor.h"

void setMotorPins(const uint8_t controlPin1, const uint8_t controlPin2) {
  pinMode(controlPin1, OUTPUT);
  pinMode(controlPin2, OUTPUT);  
}

void motorTurnOn(const uint8_t controlPin1, const uint8_t controlPin2) {
  digitalWrite (controlPin1, LOW);
  digitalWrite (controlPin2, HIGH);
}

void motorTurnOff(const uint8_t controlPin1, const uint8_t controlPin2) {
  digitalWrite (controlPin1, LOW);
  digitalWrite (controlPin2, LOW);
}

void setMotorPins(const Motor* motor) {
  pinMode(motor->controlPin1, OUTPUT);
  pinMode(motor->controlPin2, OUTPUT);  
}

void motorTurnOn(const Motor* motor) {
  digitalWrite (motor->controlPin1, LOW);
  digitalWrite (motor->controlPin2, HIGH);
}

void motorTurnOff(const Motor* motor) {
  digitalWrite (motor->controlPin1, LOW);
  digitalWrite (motor->controlPin2, LOW);
}