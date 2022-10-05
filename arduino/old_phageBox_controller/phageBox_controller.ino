// Phagebox Version 2
#include <OneWire.h> 
#include <DallasTemperature.h>



/*
 * DESCRIPTION:
 * This arduino script controls the PhageBox components by handeling 
 * input chararcters and using these to process the whether or not 
 * comonents are turned off or on.  
 * 
 * HOW TO USE:
 * Once the PhageBox is assembled, upload this script to the arduino 
 * using the serial port. This can be done by using the arduino IDE 
 * or by using the arduino CLI. 
 * 
 */



/*
 * The global variables below refer to pins on the Arduino
 * TODO: An overall goal would be to have these as a config file
 */
const int BACKLIGHT = 3;
const int MAGNET = 5;
const int FRONTTEC = 6;
const int BACKTEC = 7;
#define TEMPSENSFRONT 10
#define TEMPSENSMETAL 11
#define TEMPSENSBACK 12
#define ON   1
#define OFF  0


/*
 * Activate the temperature sensing library
 */
OneWire oneWire(TEMPSENSFRONT); 
DallasTemperature sensors(&oneWire);
OneWire oneWire1(TEMPSENSMETAL); 
DallasTemperature sensors1(&oneWire1);
OneWire oneWire2(TEMPSENSBACK); 
DallasTemperature sensors2(&oneWire2);

/*
 * This function sets the staus of a pin.
 */
void SetStatus(int pinNumber, int newStatus)
{
  digitalWrite(pinNumber, newStatus);
}

/*
 * Initialize the components
 */
void relay_init(void)//initialize the relay
{
  //set all the relays OUTPUT
  pinMode(MAGNET, OUTPUT);
  pinMode(FRONTTEC, OUTPUT);
  pinMode(BACKTEC, OUTPUT);
  SetStatus(FRONTTEC, ON); //turn off relay for front TEC module
  SetStatus(BACKTEC, ON); //turn off relay for back TEC module
  SetStatus(MAGNET, OFF); //turn off relay for magnet
  
}

/*
 * The below function takes in input per loop() and 
 * turns off and on the components of the device.
 */
void handleSerial() {
 while (Serial.available() > 0) {
   char incomingCharacter = Serial.read();
   switch (incomingCharacter) {
     // FRONT TEC CONTROL
     case '1':
      SetStatus(FRONTTEC, ON);
      break;
     case '2':
      SetStatus(FRONTTEC, OFF);
      break;

     // BACK TEC MODULE
     case '3':
      SetStatus(BACKTEC, ON);
      break;
     case '4':
      SetStatus(BACKTEC, OFF);
      break;

     // MAGNET CONTROL
     case '5':
      SetStatus(MAGNET,ON);
      break;
     case '6':
      SetStatus(MAGNET, OFF);
      break;

     // BACKLIGHT CONTROL
     case '7': //backlight on
      SetStatus(BACKLIGHT, ON);
      break;
     case '8': //backlight off
      SetStatus(BACKLIGHT, OFF);
      break;
    }
  }
}

/*
 * Set up the device. 
 * Essentially initialize all of the components.
 */
void setup()
{
  relay_init();
  pinMode(BACKLIGHT, OUTPUT);
  Serial.begin(9600);
  sensors.begin();
}

/*
 * Loop for the arrduino controlling input 
 * as well as printing temperatures to serriel monitor.
 */
void loop() 
{
  // Get temperatures
  sensors.requestTemperatures();
  Serial.print("TEC_1: ");
  Serial.print(sensors.getTempCByIndex(0));
  Serial.print("\n");
  sensors1.requestTemperatures();
  Serial.print("TEC_MET: ");
  Serial.print(sensors1.getTempCByIndex(0));
  Serial.print("\n");
  sensors2.requestTemperatures();
  Serial.print("TEC_2: ");
  Serial.print(sensors2.getTempCByIndex(0));
  Serial.print("\n");

  
  handleSerial();
  delay(1000); 
}
