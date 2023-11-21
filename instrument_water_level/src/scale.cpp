#include "..\include\scale.h"

void setScalePins(HX711* scale, const uint8_t dataPin, const uint8_t clockPin) {
  scale->begin(dataPin, clockPin);
}


void calibrateScale(HX711* scale) {
  Serial.println("\nPut 210gr in the scale, press enter to continue");
  while(!Serial.available());
  while(Serial.available()) Serial.read();
  scale->set_scale(210);

  Serial.println("\nPut an empty container in the scale, press enter to continue");
  while(!Serial.available());
  while(Serial.available()) Serial.read();

  scale->tare(20);
  Serial.print("UNITS: ");
  Serial.println(scale->get_units(10));
  

  Serial.println("\nScale is Scaled, press enter to continue");
  while(!Serial.available());
  while(Serial.available()) Serial.read();
}

bool isWeightReached(long targetWeight, long scaleValue, long tolerance) {
  if (scaleValue >= targetWeight - tolerance && scaleValue <= targetWeight + tolerance) {
    return true;
  } 
  return false;
}

void debugScale(HX711* scale, const uint8_t PinIN1, const uint8_t PinIN2, const uint8_t PinIN3, const uint8_t PinIN4) {
    Serial.print("ScaleValue ");
    Serial.println(scale->get_units()); 
    Serial.print("PinIN1 vaciado: ");
    Serial.println(digitalRead(PinIN1));
    Serial.print("PinIN2 vaciado: ");
    Serial.println(digitalRead(PinIN2));
    Serial.print("PinIN3 llenado: ");
    Serial.println(digitalRead(PinIN3));
    Serial.print("PinIN4 llenado: ");
    Serial.println(digitalRead(PinIN4));
}

