#include "configuration.h"
#include "LaserDriver.h"
#include "StepperController.h"
#include "ProcessController.h"

void setup(){
  
  Serial.begin(BAUDRATE);

  initSteppers();
  home_y_axis();
  home_z_axis();
  //moveToNextLayer();
  
  noInterrupts();
  laser_init();  
  interrupts();
  
  laser_on();
  
  
  Serial.print("Open Exposer Ready\n");
}

void loop(){
    processController(); 
}




