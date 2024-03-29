class HX711;

// Scale
const uint8_t dataPin = 10;
const uint8_t clockPin = 11; //SCK

// Scale Tolerance
extern uint8_t scaleTolerance;

// Scale Factor
extern float scaleFactor;

// Scale 
extern HX711 scale;
extern long scaleMock;

extern long targetWeight; 
extern long maxWeight;

void setScalePins();
void getCurrentUnits();
void tareScale();
bool isWeightReached(long scaleValue);
void debugScale();