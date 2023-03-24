#include "serial_parser.h"

/*
 * Descripton:
 *     This buffer holds onto the string
 *     being transmitted from the host PC.
 */
const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

// Defined in header
void getDataFromPC(TemperatureModule *temp_modules[])
{

  // receive data from PC and save it into inputBuffer

  if (Serial.available() > 0)
  {

    char x = Serial.read();
    // the order of these IF clauses is significant
    if (x == endMarker)
    {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0; // dreycey: append EOS character
      parseData(temp_modules);
    }

    if (readInProgress)
    {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd++;
      if (bytesRecvd == buffSize)
      { // if buffer overload
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker)
    {
      bytesRecvd = 0;
      readInProgress = true;
    }
  }
}

// Defined in header
void parseData(TemperatureModule *temp_modules[])
{

  // split the data into its parts
  char *strtokIndx; // this is used by strtok() as an index
  int newFlashInterval = 0;
  const char delim[2] = ",";
  char messageFromPC[buffSize] = {0};

  /*
   * Parse the input bufffer and turn into
   * expected data types.
   */
  strtokIndx = strtok(inputBuffer, delim); // get the first part - the string
  strcpy(messageFromPC, strtokIndx);       // copy it to messageFromPC

  if (messageFromPC[0] == 'H')
  {

    Serial.print("\nUpdating PCR..\n");
    // get heater #
    strtokIndx = strtok(NULL, delim);   // parse on delimm
    int heater_numb = atoi(strtokIndx); // str2int

    // get heater #
    strtokIndx = strtok(NULL, delim);   // parse on delimm
    int cycle_count = atoi(strtokIndx); // str2int

    // get Denature info
    strtokIndx = strtok(NULL, delim); // parse on delimm
    int den_time = atoi(strtokIndx);  // str2int
    strtokIndx = strtok(NULL, delim); // parse on delimm
    int den_temp = atoi(strtokIndx);  // str2int

    // get Anneal info
    strtokIndx = strtok(NULL, delim);   // parse on delimm
    int anneal_time = atoi(strtokIndx); // str2int
    strtokIndx = strtok(NULL, delim);   // parse on delimm
    int anneal_temp = atoi(strtokIndx); // str2int

    // get Extension info
    strtokIndx = strtok(NULL, delim); // parse on delimm
    int ext_time = atoi(strtokIndx);  // str2int
    strtokIndx = strtok(NULL, delim); // parse on delimm
    int ext_temp = atoi(strtokIndx);  // str2int

    // send values back for validation
    Serial.print(startMarker);
    Serial.print(cycle_count);
    Serial.print(endMarker);

    // update tempmodule
    if (heater_numb == 1)
    {
      temp_modules[0]->update_state_table(DENATURE, den_time, den_temp);
      temp_modules[0]->update_state_table(ANNEAL, anneal_time, anneal_temp);
      temp_modules[0]->update_state_table(ELONGATE, ext_time, ext_temp);
      temp_modules[0]->set_cycle_count(cycle_count);
      temp_modules[0]->start_pcr();
    }
    else if (heater_numb == 2)
    {
      temp_modules[1]->update_state_table(DENATURE, den_time, den_temp);
      temp_modules[1]->update_state_table(ANNEAL, anneal_time, anneal_temp);
      temp_modules[1]->update_state_table(ELONGATE, ext_time, ext_temp);
      temp_modules[1]->set_cycle_count(cycle_count);
      temp_modules[1]->start_pcr();
    }
  }
  else if (messageFromPC[0] == 'B')
  {
    // parse mag value
    strtokIndx = strtok(NULL, delim); // parse on delimm
    int mag_val = atoi(strtokIndx);   // str2int

    // parse LED
    strtokIndx = strtok(NULL, delim); // parse on delimm
    int led_val = atoi(strtokIndx);   // str2int

    // send values back for validation
    Serial.print(startMarker);
    Serial.print(led_val);
    Serial.print(endMarker);

    // update LED and Magnet
    if (led_val)
      toggle_pin(LED_PIN);
    if (mag_val)
      toggle_pin(RELAY_MAG);
  }
  else
  {
    Serial.print("WRONG SERIAL MSG.");
  }
}