#include "PhageBox.h"
#define TEMPMODULE_COUNT (2)

/*
 * Globals
 *    The globall temp_modules below are used for each
 *    of the temperature modules on the device.
 */
TemperatureModule *temp_modules[TEMPMODULE_COUNT] = {&front_temp_module, &back_temp_module};

// Defined in header
void init_phagebox()
{
    init_timer();
    initialize_gpio_pins();

    // turn temp relays off
    toggle_pin(BACK_TEMP_RELAY);
    toggle_pin(FRONT_TEMP_RELAY);

    Serial.println("<Arduino is ready>");

    // toggle LED to show it is on.
    for (int i = 0; i < 10; i++)
    {
        toggle_pin(LED_PIN);
        delay(100);
    }
}

// Defined in header
void start_phagebox()
{
    getDataFromPC(temp_modules);

    // if PCR is on, evaluate
    for (int i = 0; i < TEMPMODULE_COUNT; i++)
    {
        TemperatureModule *curr_temp_module = temp_modules[i];
        if (curr_temp_module->current_state != STOPPED)
        { // if ON...
            float curr_temp = curr_temp_module->getTemp();
            float desired_temp = curr_temp_module->get_desiredTemp();
            if (i == 0)
            {
                Serial.print("T_FRONT,"); // expected by GUI
                Serial.print(curr_temp);
                Serial.print("\n");
                Serial.print("T_FRONT_SET,"); // expected by GUI
                Serial.print(desired_temp);
                Serial.print("\n");
            }
            else if (i == 1)
            {
                Serial.print("T_BACK,"); // expected by GUI
                Serial.print(curr_temp);
                Serial.print("\n");
                Serial.print("T_BACK_SET,"); // expected by GUI
                Serial.print(desired_temp);
                Serial.print("\n");
            }
            // bang bang controller
            if (curr_temp <= desired_temp)
            {
                // Serial.print("ON \n");
                curr_temp_module->heater_on();
            }
            else if (curr_temp >= desired_temp)
            {
                // Serial.print("OFF \n");
                curr_temp_module->heater_off();
            }
            // go to next state or cancel
            curr_temp_module->update_states();
        }
    }
}