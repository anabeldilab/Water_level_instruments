#include "Vrekrer_scpi_parser.h"
#include "HX711.h"

#include "include/scale.h"
#include "include/motor.h"
#include "include/control_water_level.h"
#include "include/instrument.h"

void setup() {
  Serial.begin(9600);

  registerCommands();

  setScalePins();
  setMotorPins(mainMotor);
  setMotorPins(auxMotor);

  tareScale();
}


void loop() {
  my_instrument.ProcessInput(Serial, "\n");
  if (weightControl) {
    controlWaterLevel();
  }
  delay(200);
}