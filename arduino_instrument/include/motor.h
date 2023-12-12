struct Motor {
  uint8_t controlPin1;
  uint8_t controlPin2;
};

// Main motor
const uint8_t PinIN1 = 7;
const uint8_t PinIN2 = 6;

// Aux motor
const uint8_t PinIN3 = 5;
const uint8_t PinIN4 = 4;

const Motor mainMotor = {PinIN1, PinIN2};
const Motor auxMotor = {PinIN3, PinIN4};

void setMotorPins(const uint8_t controlPin1, const uint8_t controlPin2);
void motorTurnOn(const uint8_t controlPin1, const uint8_t controlPin2);
void motorTurnOff(const uint8_t controlPin1, const uint8_t controlPin2);
void setMotorPins(const Motor& motor);
void motorTurnOn(const Motor& motor);
void motorTurnOff(const Motor& motor);