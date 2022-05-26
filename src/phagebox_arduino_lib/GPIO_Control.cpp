#include "GPIO_Control.h"

// Defined in header
void initialize_gpio_pins() {
    int num_portd_gpio_pins = 4;
    for (int i =0; i < num_portd_gpio_pins; i++) {
        init_pin(portd_gpio_pins[i]);
    }
}

// Defined in header
void init_pin(int PIN_NUMBER) {
    Serial.print("Init Pin:");
    Serial.print(PIN_NUMBER);
    Serial.print("\n");
    DDRD |= (1 << PIN_NUMBER); // direction is out
    PORTD &= ~(1 << PIN_NUMBER); // start off low
}

// Defined in header
void toggle_pin(int PIN_NUMBER) {
    if ((PORTD & (1 << PIN_NUMBER)) >> PIN_NUMBER) {
        PORTD &= ~(1 << PIN_NUMBER); // low
    } else {
        PORTD |= (1 << PIN_NUMBER); // high
    }
}

// Defined in header
void toggle_pin_on(int PIN_NUMBER) {
    if (!((PORTD & (1 << PIN_NUMBER)) >> PIN_NUMBER)) {
        PORTD |= (1 << PIN_NUMBER); // high
    }
}

// Defined in header
void toggle_pin_off(int PIN_NUMBER) {
    if ((PORTD & (1 << PIN_NUMBER)) >> PIN_NUMBER)
        PORTD &= ~(1 << PIN_NUMBER); // low
}
