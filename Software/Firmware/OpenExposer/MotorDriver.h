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

#ifndef OPENEXPOSER_STEPPERCONTROLLER_H
#define OPENEXPOSER_STEPPERCONTROLLER_H

#include <Arduino.h>

// Helper Macro degrees to Microseconds for Timer2 Servo
#define degreesToMS( _degrees) (_degrees * 6 + 900)

void init_motor_driver();
void motors_release();
void do_move(float x_distcance, float y_distance, float feedrate);
void home_z_axis();
void home_y_axis();
void vat_down();
void vat_up();


#endif //OPENEXPOSER_STEPPERCONTROLLER_H
