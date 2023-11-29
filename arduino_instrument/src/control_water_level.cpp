#include "..\include\control_water_level.h"
#include "..\include\motor.h"
#include "..\include\scale.h"


void emptyContainer(const Motor* mainMotor, const Motor* auxMotor) {
  motorTurnOn(mainMotor);
  motorTurnOff(auxMotor);
}


void fillContainer(const Motor* mainMotor, const Motor* auxMotor) {
  motorTurnOff(mainMotor);
  motorTurnOn(auxMotor);
}


void waterLevelReached(const Motor* mainMotor, const Motor* auxMotor) {
  motorTurnOff(mainMotor);
  motorTurnOff(auxMotor);
}


void changeTargetWeight(long* targetWeight, const long newTargetWeight, bool* weightControl) {
  *targetWeight = newTargetWeight;
  *weightControl = true;
}


void controlWaterLevel(long targetWeight, HX711* scale, const Motor* mainMotor, const Motor* auxMotor, const long tolerance, bool* weightControl) {
  long scaleValue = scale->get_units(5);
  if (isWeightReached(targetWeight, scaleValue, tolerance)) {
    //Serial.println("Water level reached");
    //Serial.print("Units: ");
    //Serial.println(scaleValue);
    waterLevelReached(mainMotor, auxMotor);
    *weightControl = false;
  } else if (scaleValue < targetWeight) {
    //Serial.println("Filling container...");
    //Serial.print("Units: ");
    //Serial.println(scaleValue);
    fillContainer(mainMotor, auxMotor);
  } else if (scaleValue > targetWeight) {
    //Serial.println("Emptying container...");
    //Serial.print("Units: ");
    //Serial.println(scaleValue);
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