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
  interface.print("Units: ");
  interface.println(scale.get_units(10));
}


inline void setMaxWeight(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  if (parameters.Size() > 0) {
    maxWeight = constrain(String(parameters[0]).toInt(), 0, 10000);
  }
}


inline void getTargetWeight(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.print("Target Weight: ");
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


inline void registerCommands() {
  my_instrument.SetCommandTreeBase(F("TANK:LEVEL"));
  my_instrument.RegisterCommand(F(":INC"), &increaseLevel);
  my_instrument.RegisterCommand(F(":DEC"), &decreaseLevel);
  my_instrument.RegisterCommand(F(":STOP"), &waterLevelReached);
  my_instrument.RegisterCommand(F(":UNITS?"), &getUnits);
  my_instrument.RegisterCommand(F(":MAXWEIGHT"), &setMaxWeight);
  my_instrument.RegisterCommand(F(":TARGETWEIGHT?"), &getTargetWeight);
  my_instrument.RegisterCommand(F(":TARGETWEIGHT"), &setTargetWeight);
  my_instrument.RegisterCommand(F(":TARE"), &tareScale);
}
