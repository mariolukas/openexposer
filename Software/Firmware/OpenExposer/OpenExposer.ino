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




