#include "configuration.h"
#include "LaserDriver.h"
#include "StepperControl.h"
#include "ProcessCommand.h"

void setup(){
  
  Serial.begin(57600);

  initSteppers();


  noInterrupts();
  laser_init();  
  interrupts();
  
  Serial.print("Exposer Ready\n");
  laser_on();

}

void loop(){
    
      processData();
  
}




