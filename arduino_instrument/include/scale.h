#include <Arduino.h>
#include <HX711.h>

void setScalePins(HX711* scale, const uint8_t dataPin, const uint8_t clockPin);

void getCurrentUnits(HX711* scale);

void tareScale(HX711* scale);

bool isWeightReached(long targetWeight, long scaleValue, long tolerance);

void debugScale(HX711* scale, const uint8_t PinIN1, const uint8_t PinIN2, const uint8_t PinIN3, const uint8_t PinIN4);