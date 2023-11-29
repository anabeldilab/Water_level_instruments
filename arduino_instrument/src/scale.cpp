#include "..\include\scale.h"

void setScalePins(HX711* scale, const uint8_t dataPin, const uint8_t clockPin) {
  scale->begin(dataPin, clockPin);
}


void calibrateScale(HX711* scale) {
  //Serial.print("Lectura del valor del ADC:  ");
  //Serial.println(scale->read());
  //Serial.println("No ponga ningun  objeto sobre la scale");
  //Serial.println("Destarando...");
  //Serial.println("...");
  scale->set_scale(742.752312); // Establecemos la escala  ATENCIÓN 
  scale->tare(20);  //El peso actual es considerado Tara.
  
  //Serial.println("Listo para pesar");  
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

