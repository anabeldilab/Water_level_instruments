#include <Arduino.h>
#include "HX711.h"

struct Motor;

void emptyContainer(const Motor* mainMotor, const Motor* auxMotor);
void fillContainer(const Motor* mainMotor, const Motor* auxMotor);
void waterLevelReached(const Motor* mainMotor, const Motor* auxMotor);

void changeTargetWeight(long* targetWeight, const long newTargetWeight, bool* weightControl);

void controlWaterLevel(long targetWeight, HX711* scale, const Motor* mainMotor, const Motor* auxMotor, const long tolerance, bool* weightControl);
void mockControlWaterLevel(long targetWeight, long scaleMock, const long tolerance);