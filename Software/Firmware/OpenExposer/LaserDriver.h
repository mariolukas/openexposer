/**
 * OpenExposer firmware
 *
 *  Copyright 2014 by Mario Lukas <info@mariolukas.de>
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

#ifndef OPENEXPOSER_LASERDRIVER_H
#define OPENEXPOSER_LASERDRIVER_H

#include <Arduino.h>

#include "configuration.h"

typedef struct {
    uint8_t length;
    union {
        long positions[LASER_POSITIONS_BUFFER_SIZE];
        uint16_t laser_timings[LASER_POSITIONS_BUFFER_SIZE];
    };
} laser_buffer_type;

void init_laser_driver();
void laser_on();
void laser_off();
void expose_line(uint16_t cycles);
void fill_laser_buffer(int32_t distance);
void create_test_pattern();
void convert_positions_to_timings();

#endif // OPENEXPOSER_LASERDRIVER_H

