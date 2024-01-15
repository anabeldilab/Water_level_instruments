SCPI_Parser my_instrument;

inline void increaseLevel(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  fillContainer();
  weightControl = false;
}


inline void decreaseLevel(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  emptyContainer();
  weightControl = false;
}


inline void waterLevelReached(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  waterLevelReached();
  weightControl = false;
}


inline void getUnits(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.println(scale.get_units());
}


inline void setMaxWeight(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  if (parameters.Size() > 0) {
    maxWeight = constrain(String(parameters[0]).toInt(), 0, 10000);
  }
}


inline void getMaxWeight(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.println(maxWeight);
}


inline void getTargetWeight(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.println(targetWeight);
}


inline void setTargetWeight(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  if (parameters.Size() > 0) {
    targetWeight = constrain(String(parameters[0]).toInt(), -300, 900);
  }
  weightControl = true;
}


inline void tareScale(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  tareScale();
}


inline void getWaterLevelReached(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.println(!weightControl);
}


inline void getScaleTolerance(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.println(scaleTolerance);
}


inline void setScaleTolerance(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  if (parameters.Size() > 0) {
    scaleTolerance = constrain(String(parameters[0]).toInt(), 0, 1000);
  }
}


inline void calibrateScale(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  if (parameters.Size() > 0) {
    float knownWeight = String(parameters[0]).toFloat();
    scaleFactor = scale.get_value(10) / knownWeight;
    scale.set_scale(scaleFactor);
    if (scale.get_units(5) < 0) {
      scaleFactor = -scaleFactor;
      scale.set_scale(scaleFactor);
    }
  }
}


inline void registerCommands() {
  my_instrument.SetCommandTreeBase(F("TANK:LEVEL"));
  my_instrument.RegisterCommand(F(":INC"), &increaseLevel);
  my_instrument.RegisterCommand(F(":DEC"), &decreaseLevel);
  my_instrument.RegisterCommand(F(":STOP"), &waterLevelReached);
  my_instrument.RegisterCommand(F(":UNITS?"), &getUnits);
  my_instrument.RegisterCommand(F(":MAXWEIGHT"), &setMaxWeight);
  my_instrument.RegisterCommand(F(":MAXWEIGHT?"), &getMaxWeight);
  my_instrument.RegisterCommand(F(":TARGETWEIGHT?"), &getTargetWeight);
  my_instrument.RegisterCommand(F(":TARGETWEIGHT"), &setTargetWeight);
  my_instrument.RegisterCommand(F(":WATERLEVELREACHED?"), &getWaterLevelReached);
  my_instrument.RegisterCommand(F(":TARE"), &tareScale);
  my_instrument.RegisterCommand(F(":TOLERANCE?"), &getScaleTolerance);
  my_instrument.RegisterCommand(F(":TOLERANCE"), &setScaleTolerance);
  my_instrument.RegisterCommand(F(":CALIBRATE"), &calibrateScale);
}
