/*
 * Descripton:
 *     This module controls the GPIO pins
 *     and contains information about the GPIO
 *     peripherals on the PhageBox.
 */
#ifndef GPIO_Control_h
#define GPIO_Control_h
// GPIO Defines.
#define LED_PIN (3)
#define RELAY_MAG (5)
#define FRONT_TEMP_RELAY (6)     // front relay
#define BACK_TEMP_RELAY (7)      // back relay
#define METAL_TEMPSENSE_PIN (10) // front metal
#define FRONT_TEMPSENSE_PIN (11) // front plastic
#define BACK_TEMPSENSE_PIN (12)  // back

// Check Arduino
#if (ARDUINO >= 100)
#include <Arduino.h>
#else
#include <WProgram.h>
#include <pins_arduino.h>
#endif

// list with all GPIO pins for referencing.
const int portd_gpio_pins[4] = {LED_PIN, RELAY_MAG, BACK_TEMP_RELAY, FRONT_TEMP_RELAY};

/*
 * Function:
 *     init_led()
 * Description:
 *     Activates the phagebox LED
 * Input:
 *     1. PIN Number for port D
 * Output:
 *     void/NA
 * Error Handling:
 *     void/NA
 */
void init_pin(int PIN_NUMBER);

/*
 * Function:
 *     toggle_pin();
 * Description:
 *     toggles the LED on or off
 * Input:
 *     1. PIN Number for port D
 * Output:
 *     void/NA
 * Error Handling:
 *     void/NA
 */
void toggle_pin(int PIN_NUMBER);

/*
 * Function:
 *     initialize_gpio_pins()
 * Description:
 *     initializes all of the pins on port D
 * Input:
 *     void/NA
 * Output:
 *     void/NA
 * Error Handling:
 *     void/NA
 */
void initialize_gpio_pins();

/*
 * Function:
 *     toggle_pin_on()
 * Description:
 *     toggles a specified pin to be on.
 * Input:
 *     void/NA
 * Output:
 *     void/NA
 * Error Handling:
 *     void/NA
 */
void toggle_pin_on(int PIN_NUMBER);

/*
 * Function:
 *     toggle_pin_off()
 * Description:
 *     toggles a specified pin to be off
 * Input:
 *     void/NA
 * Output:
 *     void/NA
 * Error Handling:
 *     void/NA
 */
void toggle_pin_off(int PIN_NUMBER);

#endif