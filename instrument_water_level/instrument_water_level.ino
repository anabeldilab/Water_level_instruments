#include "HX711.h"
#include "Vrekrer_scpi_parser.h"

const uint8_t PinIN1 = 7;
const uint8_t PinIN2 = 6;
const uint8_t PinIN3 = 5;
const uint8_t PinIN4 = 4;
const uint8_t dataPin = 10;
const uint8_t clockPin = 11; //SCK

const uint8_t TOLERANCE = 5;

long scaleMock = 400;

long targetWeight = 0;

HX711 scale;
SCPI_Parser my_instrument;

void setup() {
  my_instrument.RegisterCommand(F("*IDN?"), &Identify);
  my_instrument.SetCommandTreeBase(F("SYSTem:"));
    my_instrument.RegisterCommand(F(":BRIGhtness"), &SetBrightness);
    my_instrument.RegisterCommand(F(":BRIGhtness?"), &GetBrightness);
    my_instrument.RegisterCommand(F(":BRIGhtness:INCrease"), &IncDecBrightness);
    my_instrument.RegisterCommand(F(":BRIGhtness:DECrease"), &IncDecBrightness);
  Serial.begin(9600);

  scale.begin(dataPin, clockPin);

  Serial.print("UNITS: ");
  Serial.println(scale.get_units(10));

  Serial.println("Do you want to calibrate the terminal? 0 o 1");
  uint8_t calibration = terminalRead();
  if (calibration) {
    Serial.println("\nPut 530gr in the scale, press enter to continue");
    while(!Serial.available());
    while(Serial.available()) Serial.read();
    scale.set_scale(530.f);

    Serial.println("\nPut an empty container in the scale, press enter to continue");
    while(!Serial.available());
    while(Serial.available()) Serial.read();

    scale.tare(20);
    Serial.print("UNITS: ");
    Serial.println(scale.get_units(10));
    

    Serial.println("\nScale is calibrated, press enter to continue");
    while(!Serial.available());
    while(Serial.available()) Serial.read();
  }

  pinMode(PinIN1, OUTPUT); // motor 1
  pinMode(PinIN2, OUTPUT); // motor 1
  pinMode(PinIN3, OUTPUT); // motor 2
  pinMode(PinIN4, OUTPUT); // motor 2

  Serial.print("Peso actual: ");
  Serial.println(scale.get_units(10));
  Serial.println("Introduzca un peso deseado inicial: ");
  targetWeight = terminalRead();
  Serial.println();
}

void loop() {
  Serial.println("No ha leido scale"); 
  long scaleValue = scale.get_units();
  Serial.println("Leido scale"); 

  if (scaleValue >= targetWeight - TOLERANCE && scaleValue <= targetWeight + TOLERANCE) {
  //if (scaleMock >= targetWeight - TOLERANCE && scaleMock <= targetWeight + TOLERANCE) {
    /*Serial.print("ScaleMock ");
    Serial.println(scaleMock); */

    Serial.print("ScaleValue ");
    Serial.println(scaleValue); 
    Serial.print("PinIN1 vaciado: ");
    Serial.println(digitalRead(PinIN1));
    Serial.print("PinIN2 vaciado: ");
    Serial.println(digitalRead(PinIN2));
    Serial.print("PinIN3 llenado: ");
    Serial.println(digitalRead(PinIN3));
    Serial.print("PinIN4 llenado: ");
    Serial.println(digitalRead(PinIN4));

    MotorStop(PinIN1, PinIN2); // Motor Primario
    MotorStop(PinIN3, PinIN4); // Motor Secundario
    Serial.println("Introduzca un peso1: ");
    targetWeight = terminalRead();
    Serial.println();
  } else if (scaleValue < targetWeight /*scaleMock < targetWeight*/) { // llenado
    scaleMock++;
    /*Serial.print("ScaleMock ");
    Serial.println(scaleMock); */

    Serial.print("ScaleValue ");
    Serial.println(scaleValue); 

    vaciarContenedor();

    Serial.print("PinIN1 vaciado: ");
    Serial.println(digitalRead(PinIN1));
    Serial.print("PinIN2 vaciado: ");
    Serial.println(digitalRead(PinIN2));
    Serial.print("PinIN3 llenado: ");
    Serial.println(digitalRead(PinIN3));
    Serial.print("PinIN4 llenado: ");
    Serial.println(digitalRead(PinIN4));
  } else if (scaleValue > targetWeight /*scaleMock > targetWeight*/) {
    scaleMock--;
    /*Serial.print("ScaleMock ");
    Serial.println(scaleMock);*/

    Serial.print("ScaleValue ");
    Serial.println(scaleValue); 

    llenarContenedor();

    Serial.print("PinIN1 vaciado: ");
    Serial.println(digitalRead(PinIN1));
    Serial.print("PinIN2 vaciado: ");
    Serial.println(digitalRead(PinIN2));
    Serial.print("PinIN3 llenado: ");
    Serial.println(digitalRead(PinIN3));
    Serial.print("PinIN4 llenado: ");
    Serial.println(digitalRead(PinIN4));
    Serial.println();
  }
  delay(200);
}

void vaciarContenedor() {
  Serial.println("Motor izquierdo Detenido"); 
  MotorStop(PinIN1, PinIN2);
  Serial.println("Motor derecho PRINCIPAL echa agua");
  MotorEchaAgua(PinIN3, PinIN4);
}

void llenarContenedor() {
  Serial.println("Motor derecho PRINCIPAL Detenido");
  MotorStop(PinIN3, PinIN4);
  Serial.println("Motor izquiedo echa agua");
  MotorEchaAgua(PinIN1, PinIN2);
}

void MotorEchaAgua(int pinIN1Motor, int pinIN2Motor) {
  digitalWrite (pinIN1Motor, LOW);
  digitalWrite (pinIN2Motor, HIGH);
}

void MotorStop(int pinIN1Motor, int pinIN2Motor) {
  digitalWrite (pinIN1Motor, LOW);
  digitalWrite (pinIN2Motor, LOW);
}

long terminalRead() {
  String incomingString = "";
  long convertion;
  while (!Serial.available());

  incomingString = Serial.readString();
    
  if (incomingString.length() >= 1) {
    incomingString.remove(incomingString.length() - 1);
    
    Serial.print("I received: ");
    Serial.println(incomingString);
  }
  convertion = incomingString.toInt();
  Serial.print("Convertion: ");
  Serial.println(convertion);    

  return convertion;
}
