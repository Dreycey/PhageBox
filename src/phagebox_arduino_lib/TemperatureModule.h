/*
 * Descripton:
 *     This module contains the data strutures
 *     for creatinig temperature control modules.
 *     Each of these modules contains it's own
 *     finite state machine using a table implpimentation.
 */
#ifndef  TemperatureModule_h                                                            
#define TemperatureModule_h                                            
#include "OneWire.h"
#include "DallasTemperature.h"
#include "GPIO_Control.h"
#include "timer.h"
#define NUM_STATES (4)

// Check Arduino                                                                          
#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
 #include <pins_arduino.h>
#endif

/*
 * pcr_state
 *
 *     This enum describes the different PCR states
 *     available.
 * 
 * NOTE: if you add to this update NUM_STATES
 */
typedef enum pcr_state {
	STOPPED = 0,
	DENATURE = 1,
	ANNEAL = 2,
	ELONGATE = 3,
} pcr_state;

/*
 * States
 *
 *    This table describes the states
 *    the finite state machine may have.
 *    Note these state are based on PCR. 
 */
struct States {
	pcr_state current_state;
	int time;
	int temp;
	pcr_state next_state;
};

/*
 * Class: 
 *     TemperatureModule 
 * Description:
 *     This class creates a temperature control module, having access
 *     to both a heater and a temperature sensor. This class holds a table-based
 *     finite state machine representing PCR for processing the temperature.
 * Input:
 *     void/NA
 * Output: 
 *     void/NA
 * Error Handling:
 *     void/NA
 */
class TemperatureModule 
{
public:

	TemperatureModule(uint8_t relay_pin, uint8_t tempsense_pin, volatile int* timer);

	// update the state table with new values. 
    void update_state_table(pcr_state state, int time, int temp);

	// go to next state
	void go2nextstate() {current_state = state_table[current_state].next_state;};
	void update_states();

	//start and stop PCR from running.
	void start_pcr();
	void stop_pcr();

    // get the current temperature
    float getTemp();
	void toggle_relay();
    void heater_on();
	void heater_off();
    pcr_state current_state;

	// setters and getters
	int get_currentTimeLen();
	float get_desiredTemp();
	void set_cycle_count(int cycle_count);

private:
	typedef uint8_t ScratchPad[9];
	uint8_t relayPin;
	DallasTemperature temp_sensor;
	float current_temperature;
	int cycle_count = 0;
	int number_cycles_used = 0;
	volatile int* internal_timer;
	/*
	* state_table
	* ------------------
	* For this particular FSM, we define the following
	* table for each state, containing information on
	* delay times, next state, and the state's color.
	*/
	struct States state_table[NUM_STATES] = 
	{
		{STOPPED, 0, 0, STOPPED},
		{DENATURE, 0, 0, ANNEAL},
		{ANNEAL, 0, 0, ELONGATE},
		{ELONGATE, 0, 0, DENATURE}
	};
};

/*
 * Global temperature sensors
 */
static TemperatureModule front_temp_module(FRONT_TEMP_RELAY, FRONT_TEMPSENSE_PIN, get_timer_1()); // front
static TemperatureModule back_temp_module(BACK_TEMP_RELAY, BACK_TEMPSENSE_PIN, get_timer_2()); // back


#endif

