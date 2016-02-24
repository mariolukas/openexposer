//
// Created by christoph on 2/23/16.
//

#ifndef OPENEXPOSER_ARDUINO_H
#define OPENEXPOSER_ARDUINO_H

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <FakeSerial.h>

#define F(x) x
#define ISR(x) void x()

#define delay(x)
#define digitalWrite(x, y)
#define digitalRead(x) LOW
#define pinMode(x, y)
#define delayMicroseconds(x)
#define micros() 0

typedef bool boolean;

#define HIGH 1
#define LOW 0

#define A0 14
#define A1 15
#define A2 16
#define A3 17
#define A4 18
#define A5 19

extern uint8_t DDRB;
extern uint8_t PORTB;
extern uint8_t DDRD;
extern uint8_t PORTD;

extern FakeSerial Serial;

#define max(x,y) (x > y ? x : y)
#define constrain(x, min, max) (x > max ? max : (x < min ? min : x ))



#endif //OPENEXPOSER_ARDUINO_H
