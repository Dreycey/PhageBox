/********************************************************************/
// First we include the libraries
#include <OneWire.h> 
#include <DallasTemperature.h>
/********************************************************************/
// Data wire is plugged into pin 2 on the Arduino 
#define ONE_WIRE_BUS_FRONT 11
#define ONE_WIRE_BUS_BACK 12
/********************************************************************/
// Setup a oneWire instance to communicate with any OneWire devices  
// (not just Maxim/Dallas temperature ICs) 
OneWire oneWire_front(ONE_WIRE_BUS_FRONT); 
OneWire oneWire_back(ONE_WIRE_BUS_BACK); 
/********************************************************************/
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors_front(&oneWire_front);
DallasTemperature sensors_back(&oneWire_back);
/********************************************************************/ 
void setup(void) 
{
 // start serial port 
 Serial.begin(9600); 
 Serial.println("Arduino Sketch for testing the top of the chip during simulated PCR"); 
 // Start up the library 
 sensors_front.begin(); 
 sensors_back.begin();
}

void loop(void) 
{ 
 // call sensors.requestTemperatures() to issue a global temperature 
 // request to all devices on the bus 
/********************************************************************/
 sensors_front.requestTemperatures(); // Send the command to get temperature readings 
 sensors_back.requestTemperatures();
/********************************************************************/
 Serial.print(sensors_front.getTempCByIndex(0)); 
 Serial.print(",");
 Serial.print(sensors_back.getTempCByIndex(0)); 
  Serial.println(""); 

// delay(100); 
} 
