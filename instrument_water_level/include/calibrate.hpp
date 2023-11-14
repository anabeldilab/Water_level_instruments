#include "HX711.h"

class Calibrate {
 public:
  Calibrate(HX711 scale, uint8_t tolerance, uint8_t pinIN1, uint8_t pinIN2, uint8_t pinIN3, uint8_t pinIN4);
  void calibrate();
  void setTargetWeight(long targetWeight);
  void setScaleMock(long scaleMock);
  long getScaleMock();
  long getTargetWeight();
 private:
  HX711 scale;
  uint8_t tolerance;
  uint8_t pinIN1;
  uint8_t pinIN2;
  uint8_t pinIN3;
  uint8_t pinIN4;
  long scaleMock;
  long targetWeight;
};