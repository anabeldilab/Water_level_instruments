#include <Arduino.h>
#include <HX711.h>

#include "../include/control_water_level.h"
#include "../include/motor.h"
#include "../include/scale.h"

bool weightControl = false;

void emptyContainer() {
  motorTurnOn(mainMotor);
  motorTurnOff(auxMotor);
}


void fillContainer() {
  motorTurnOff(mainMotor);
  motorTurnOn(auxMotor);
}


void waterLevelReached() {
  motorTurnOff(mainMotor);
  motorTurnOff(auxMotor);
}


void changeTargetWeight(const long newTargetWeight) {
  targetWeight = newTargetWeight;
  weightControl = true;
}


void controlWaterLevel() {
  long scaleValue = scale.get_units();
if (isWeightReached(scaleValue) || scaleValue >= maxWeight) {
    waterLevelReached();
    weightControl = false;
  } else if (scaleValue < targetWeight) {
    fillContainer();
  } else if (scaleValue > targetWeight) {
    emptyContainer();
  }
}


void mockControlWaterLevel() {
  if (scaleMock >= targetWeight - TOLERANCE && scaleMock <= targetWeight + TOLERANCE) {
    Serial.print("ScaleMock ");
    Serial.println(scaleMock); 
  } else if (scaleMock < targetWeight) {
    scaleMock++;
    Serial.print("ScaleMock ");
    Serial.println(scaleMock); 
  } else if (scaleMock > targetWeight) {
    scaleMock--;
    Serial.print("ScaleMock ");
    Serial.println(scaleMock);
  }
}