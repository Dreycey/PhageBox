/********************************************************************/
// First we include the libraries
#include <OneWire.h>
#include <DallasTemperature.h>
/********************************************************************/
#define ONE_WIRE_BUS 11
/********************************************************************/
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup(void)
{
  // start serial port
  Serial.begin(9600);
  sensors.begin(); // Start up the library
}

void loop(void)
{
  sensors.requestTemperatures();            // Send the command to get temperature readings
  Serial.print(sensors.getTempCByIndex(0)); // Why "byIndex"?
  Serial.print("\n");
  delay(300);
}
