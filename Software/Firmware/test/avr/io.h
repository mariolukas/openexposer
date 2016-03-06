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

#ifndef _AVR_IO_H_
#define _AVR_IO_H_

#include <stdint.h>

/* Timer 1 */
extern uint16_t ICR1;
#define ICR1L   *((uint8_t*) (void*) &ICR1);
#define ICR1H   *((uint8_t*) ((void*) &ICR1) + 1);

extern uint16_t OCR1B;
#define OCR1BL   *((uint8_t*) (void*) &OCR1B);
#define OCR1BH   *((uint8_t*) ((void*) &OCR1B) + 1);

extern uint16_t OCR1A;
#define OCR1AL   *((uint8_t*) (void*) &OCR1A);
#define OCR1AH   *((uint8_t*) ((void*) &OCR1A) + 1);

extern uint16_t TCNT1;
#define TCNT1L   *((uint8_t*) (void*) &TCNT1);
#define TCNT1H   *((uint8_t*) ((void*) &TCNT1) + 1);

extern uint8_t TCCR1B;
extern uint8_t TCCR1A;

/* TCCR1A */
#define COM1A1  7
#define COM1A0  6
#define COM1B1  5
#define COM1B0  4
#define FOC1A   3
#define FOC1B   2
#define WGM11   1
#define WGM10   0

/* TIMSK */
#define OCIE2   7
#define TOIE2   6
#define ICIE1  5
#define OCIE1A  4
#define OCIE1B  3
#define TOIE1   2
#define OCIE0   1
#define TOIE0   0

extern uint8_t TIMSK1;
extern uint8_t TIFR1;


/* Timer 2 */
extern uint8_t OCR2;
extern uint8_t TCNT2;
extern uint8_t TCCR2;

extern uint8_t TCCR2B;
extern uint8_t TCCR2A;

#define OCF1A   4
extern uint8_t SFIOR;

extern uint8_t OSCCAL;
#define OCDR    OSCCAL



/* TIFR */
#define OCF2    7
#define TOV2    6
#define ICF1    5
#define OCF1A   4
#define OCF1B   3
#define TOV1    2
#define OCF0    1
#define TOV0    0


#endif /* _AVR_IO_H_ */
