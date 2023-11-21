#include "..\include\control_water_level.h"
#include "..\include\motor.h"
#include "..\include\scale.h"


void emptyContainer(Motor* mainMotor, Motor* auxMotor) {
  motorTurnOn(mainMotor);
  motorTurnOff(auxMotor);
}


void fillContainer(Motor* mainMotor, Motor* auxMotor) {
  motorTurnOff(mainMotor);
  motorTurnOn(auxMotor);
}


void waterLevelReached(Motor* mainMotor, Motor* auxMotor) {
  motorTurnOff(mainMotor);
  motorTurnOff(auxMotor);
}


void controlWaterLevel(long targetWeight, HX711* scale, Motor* mainMotor, Motor* auxMotor, const long tolerance) {
  long scaleValue = scale->get_units(5);
  if (isWeightReached(targetWeight, scaleValue, tolerance)) {
    Serial.println("Water level reached");
    Serial.print("Units: ");
    Serial.println(scaleValue);
    waterLevelReached(mainMotor, auxMotor);
  } else if (scaleValue < targetWeight) {
    Serial.println("Filling container...");
    Serial.print("Units: ");
    Serial.println(scaleValue);
    fillContainer(mainMotor, auxMotor);
  } else if (scaleValue > targetWeight) {
    Serial.println("Emptying container...");
    Serial.print("Units: ");
    Serial.println(scaleValue);
    emptyContainer(mainMotor, auxMotor);
  }
}


void mockControlWaterLevel(long targetWeight, long scaleMock, const long tolerance) {
  if (scaleMock >= targetWeight - tolerance && scaleMock <= targetWeight + tolerance) {
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