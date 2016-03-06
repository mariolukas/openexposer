/**
 * Configuration of OpenExposer firmware
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

#ifndef OPENEXPOSER_CONFIGURATION_H
#define OPENEXPOSER_CONFIGURATION_H
        
// GENERAL
#define VERSION              (0.3)  // firmware version
#define BAUD                 (9600)  // How fast is the Arduino talking?
#define MAX_SERIAL_BUFFER    (64)  // What is the longest message Arduino can store?
        
        
// STEPPER  


#define VAT_SERVO_PIN A0

#define Z_ENABLE_PIN  2
#define Z_STEP_PIN    3
#define Z_DIR_PIN     4

#define Y_ENABLE_PIN   5  
#define Y_STEP_PIN     6  
#define Y_DIR_PIN      7


#define Y_STEPS_PER_MM 4000
#define Z_STEPS_PER_MM 16000

#define Y_RESOLUTION Z_STEPS_PER_MM  // equals 1/10 mm
#define Z_RESOLUTION Y_STEPS_PER_MM  // equals 1/10 mm

#define STEPS_PER_TURN 200
#define MICROSTEP   A5 


// ENDSTOPS
#define Y_ENDSTOP  A4
#define Z_ENDSTOP  A3

// LASER
#define LASER_PIN         9
#define LASER_PORT        B
#define LASER_BIT         1
#define LASER_PWM_PORT    D
#define LASER_PWM_BIT     6
#define LASER_PWM_PIN     6

#define LASER_EXPOSING_CYCLES 1000
#define LASER_POINT_SCALER 15

#define LASER_TIMING_SCALE_DIVIDEND 2
#define LASER_TIMING_SCALE_DIVISOR 3

#define LASER_TIMING_CENTER_OFFSET 25000

#define LASER_POSITIONS_BUFFER_SIZE 255

// OPTO TRIGGER PIN
#define OPTO_PIN 8

#define SERVO_MAX_POS 90
#define SERVO_MIN_POS 30

// USEFUL MACROS DO NOT CHANGE

#define PORT_(port) PORT ## port 
#define DDR_(port)  DDR  ## port 
#define PIN_(port)  PIN  ## port 

#define PORT(port) PORT_(port) 
#define DDR(port)  DDR_(port) 
#define PIN(port)  PIN_(port)

#define SET_DDR(p)    DDR(p##_PORT) |= (1<<p##_BIT)
#define CLEAR_DDR(p)  DDR(p##_PORT) &= ~(1<<p##_BIT)
#define OUTPUT_ON(p)  PORT(p##_PORT) |= (1<<p##_BIT)
#define OUTPUT_OFF(p) PORT(p##_PORT) &= ~(1<<p##_BIT)
#define _INPUT(p)    ((PIN(p##_PORT) & (1<<p##_BIT)) != 0)

#endif // OPENEXPOSER_CONFIGURATION_H




