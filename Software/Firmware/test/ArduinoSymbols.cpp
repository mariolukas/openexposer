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

#include <stdint.h>

#include <Arduino.h>


/* Timer 1 */
uint16_t ICR1 = 0;
uint16_t OCR1B = 0;
uint16_t OCR1A = 0;
uint16_t TCNT1 = 0;
uint8_t TCCR1B = 0;
uint8_t TCCR1A = 0;
uint8_t TIMSK1 = 0;
uint8_t TIFR1 = 0;


/* Timer 2 */
uint8_t OCR2 = 0;
uint8_t TCNT2 = 0;
uint8_t TCCR2 = 0;

uint8_t TCCR2B = 0;
uint8_t TCCR2A = 0;

uint8_t SFIOR = 0;

uint8_t OSCCAL = 0;

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
