#include "Vrekrer_scpi_parser.h"
#include <Arduino.h>
#include "HX711.h"

#include "include/scale.h"
#include "include/motor.h"
#include "include/control_water_level.h"

// Main motor
const uint8_t PinIN1 = 7;
const uint8_t PinIN2 = 6;

// Aux motor
const uint8_t PinIN3 = 5;
const uint8_t PinIN4 = 4;

// Scale
const uint8_t dataPin = 10;
const uint8_t clockPin = 11; //SCK

// Scale tolerance
const uint8_t TOLERANCE = 5;

// Scale 
HX711 scale;
long scaleMock = 400;

const Motor mainMotor = {PinIN1, PinIN2};
const Motor auxMotor = {PinIN3, PinIN4};

long targetWeight = 0; 

SCPI_Parser my_instrument;

void setup() {
  Serial.begin(9600);

  setScalePins(&scale, dataPin, clockPin);

  Serial.print("UNITS: ");
  float currentUnits = scale.get_units(10);
  Serial.println(currentUnits);

  Serial.println("Do you want to calibrate the terminal? 0 o 1");
  uint8_t calibration = terminalRead();
  if (calibration) {
    calibrateScale(&scale);
  }

  setMotorPins(&mainMotor);
  setMotorPins(&auxMotor);

  Serial.print("Peso actual: ");
  Serial.println(scale.get_units(10));
  Serial.println("Introduzca un peso deseado inicial: ");
  targetWeight = terminalRead();
  Serial.println();
}

void loop() {
  controlWaterLevel(targetWeight, &scale, &mainMotor, &auxMotor, TOLERANCE);
  delay(200);
}

long terminalRead() {
  String incomingString = "";
  long convertion;
  while (!Serial.available());

  incomingString = Serial.readString();
    
  if (incomingString.length() >= 1) {
    incomingString.remove(incomingString.length() - 1);
    
    Serial.print("I received: ");
    Serial.println(incomingString);
  }
  convertion = incomingString.toInt();
  Serial.print("Convertion: ");
  Serial.println(convertion);    

  return convertion;
}
