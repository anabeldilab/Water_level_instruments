#include <Arduino.h>
#include "HX711.h"

struct Motor;

void emptyContainer(Motor* mainMotor, Motor* auxMotor);
void fillContainer(Motor* mainMotor, Motor* auxMotor);
void waterLevelReached(Motor* mainMotor, Motor* auxMotor);

void changeTargetWeight(long* targetWeight, const long newTargetWeight, bool* weightControl);

void controlWaterLevel(long targetWeight, HX711* scale, Motor* mainMotor, Motor* auxMotor, const long tolerance, bool* weightControl);
void mockControlWaterLevel(long targetWeight, long scaleMock, const long tolerance);