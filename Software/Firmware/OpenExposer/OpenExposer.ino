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

#include "configuration.h"
#include "LaserDriver.h"
#include "MotorDriver.h"
#include "Interpreter.h"

void setup(){
  
  
  Serial.begin(BAUD);

  init_motor_driver();
  
  noInterrupts();
  init_laser_driver();  
  interrupts();
  laser_off();
  
  help();
  ready();


  
}

void loop(){

  
   while(Serial.available() > 0) {  // if something is available
    char c=Serial.read();  // get it
    if(c=='\r') continue;  // skip it
    Serial.print(c);  // repeat it back so I know you got the message
    if(sofar<MAX_SERIAL_BUFFER) buffer[sofar++]=c;  // store it
    if(c=='\n') {  // entire message received
      // we got a message and it ends with a semicolon
      buffer[sofar]=0;  // end the buffer so string functions work right
      processCommand();  // do something with the command
      ready();
    }
  }
}




