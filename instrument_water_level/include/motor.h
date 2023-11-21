#include <Arduino.h>

struct Motor {
  uint8_t controlPin1;
  uint8_t controlPin2;
};

void setMotorPins(const uint8_t controlPin1, const uint8_t controlPin2);
void motorTurnOn(const uint8_t controlPin1, const uint8_t controlPin2);
void motorTurnOff(const uint8_t controlPin1, const uint8_t controlPin2);
void setMotorPins(const Motor* motor);
void motorTurnOn(const Motor* motor);
void motorTurnOff(const Motor* motor);