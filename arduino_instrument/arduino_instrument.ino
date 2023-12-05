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
bool weightControl = false;

SCPI_Parser my_instrument;

void setup() {
  Serial.begin(9600);

  my_instrument.SetCommandTreeBase(F("TANK:LEVEL"));
  my_instrument.RegisterCommand(F(":INC"), &increaseLevel);
  my_instrument.RegisterCommand(F(":DEC"), &decreaseLevel);
  my_instrument.RegisterCommand(F(":STOP"), &waterLevelReached);
  my_instrument.RegisterCommand(F(":UNITS?"), &getUnits);
  my_instrument.RegisterCommand(F(":TARGETWEIGHT?"), &getTargetWeight);
  my_instrument.RegisterCommand(F(":TARGETWEIGHT"), &setTargetWeight);

  setScalePins(&scale, dataPin, clockPin);
  setMotorPins(&mainMotor);
  setMotorPins(&auxMotor);

  calibrateScale(&scale);
}


void loop() {
  my_instrument.ProcessInput(Serial, "\n");
  if (weightControl) {
    controlWaterLevel(targetWeight, &scale, &mainMotor, &auxMotor, TOLERANCE, &weightControl);
  }
  delay(200);
}


void increaseLevel(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  fillContainer(&mainMotor, &auxMotor);
  weightControl = false;
}


void decreaseLevel(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  emptyContainer(&mainMotor, &auxMotor);
  weightControl = false;
}


void waterLevelReached(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  waterLevelReached(&mainMotor, &auxMotor);
  weightControl = false;
}


void getUnits(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.print("Units: ");
  interface.println(scale.get_units(10));
}


void getTargetWeight(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.print("Target Weight: ");
  interface.println(targetWeight);
}


void setTargetWeight(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  if (parameters.Size() > 0) {
    targetWeight = constrain(String(parameters[0]).toInt(), -300, 900);
  }
  weightControl = true;
}
