/**
 * OpenExposer firmware
 *
 *  Copyright 2016 by Christoph Emonds <info@christoph-emonds.de>
 *
 * This file is part of OpenExposer firmware.
 *
 * OpenExposer firmware is free software: you can redistribute
 * it and/or modify it under the terms of the GNU General Public
 * License as published by the Free Software Foundation, either
 * version 3 of the License, or (at your option) any later version.
 *
 * OpenExposer firmware is distributed in the hope that it will
 * be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 * of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
 *
 * @license GPL-3.0+ <http://opensource.org/licenses/GPL-3.0>
 */

#ifndef OPENEXPOSER_ARDUINO_H
#define OPENEXPOSER_ARDUINO_H

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "FakeSerial.h"

#define F(x) x
#define ISR(x) void x()

typedef bool boolean;

#define HIGH 1
#define LOW 0

void delay(long time);
void digitalWrite(int pin, boolean value);
boolean digitalRead(int pin);

#define pinMode(x, y)
#define delayMicroseconds(x)
#define micros() 0


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
