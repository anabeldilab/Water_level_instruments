#include "calibrate.hpp"

Calibrate::Calibrate(HX711 scale, uint8_t tolerance, uint8_t pinIN1, uint8_t pinIN2, uint8_t pinIN3, uint8_t pinIN4) {
  this->scale = scale;
  this->tolerance = tolerance;
  this->pinIN1 = pinIN1;
  this->pinIN2 = pinIN2;
  this->pinIN3 = pinIN3;
  this->pinIN4 = pinIN4;
}

void Calibrate::calibrate() {
  Serial.println("\nPut 530gr in the scale, press enter to continue");
  while(!Serial.available());
  while(Serial.available()) Serial.read();
  scale.set_scale(1);

  Serial.println("\nPut an empty container in the scale, press enter to continue");
  while(!Serial.available());
  while(Serial.available()) Serial.read();

  scale.tare(20);
  Serial.print("UNITS: ");
  Serial.println(scale.get_units(10));
  

  Serial.println("\nScale is calibrated, press enter to continue");
  while(!Serial.available());
  while(Serial.available()) Serial.read();
}

void Calibrate::setTargetWeight(long targetWeight) {
  this->targetWeight = targetWeight;
}

void Calibrate::setScaleMock(long scaleMock) {
  this->scaleMock = scaleMock;
}

long Calibrate::getScaleMock() {
  return this->scaleMock;
}

long Calibrate::getTargetWeight() {
  return this->targetWeight;
}

