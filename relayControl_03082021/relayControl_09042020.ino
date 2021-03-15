// Phagebox Version 2
#include <OneWire.h> 
#include <DallasTemperature.h>

// Relay controls
//
// Assignments
//
//the relays connect to
const int IN1 = 5;
const int IN2 = 6;
#define ONE_WIRE_BUS 11
#define ON   0
#define OFF  1


OneWire oneWire(ONE_WIRE_BUS); 
DallasTemperature sensors(&oneWire);

//
//Functions
//
//set the status of relay 1
void relay_SetStatus1( unsigned char status_1)
{
  digitalWrite(IN1, status_1);
}

//set the status of relay 2
void relay_SetStatus2(unsigned char status_2)
{
  digitalWrite(IN2, status_2);
}

void relay_init(void)//initialize the relay
{
  //set all the relays OUTPUT
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  relay_SetStatus1(OFF); //turn off relay 1
  relay_SetStatus1(OFF); //turn off relay 2
}

void handleSerial() {
 while (Serial.available() > 0) {
   char incomingCharacter = Serial.read();
   switch (incomingCharacter) {
     case '1':
      relay_SetStatus1(ON);
      break;
 
     case '2':
      relay_SetStatus1(OFF);
      break;
      
     case '3':
      relay_SetStatus2(ON);
      break;
 
     case '4':
      relay_SetStatus2(OFF);
      break;
    }
  }
}

//
// Skript
//
void setup()
{
  relay_init();
  Serial.begin(9600);
  sensors.begin();
}

void loop() 
{
  sensors.requestTemperatures();
  Serial.print("TEC_1: ");
  Serial.print(sensors.getTempCByIndex(0));
  Serial.print("\n");
  handleSerial();
  delay(1000); 
}
