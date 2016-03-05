#include <stdint.h>

#include "Arduino.h"

void delay(long) {

}

void digitalWrite(int, boolean) {

}

boolean digitalRead(int) {
    return LOW;
}

uint8_t DDRB = 0;
uint8_t PORTB = 0;
uint8_t DDRD = 0;
uint8_t PORTD = 0;
