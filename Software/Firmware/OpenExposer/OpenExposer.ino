#include "configuration.h"
#include "LaserDriver.h"
#include "StepperController.h"
#include "ProcessController.h"

int pressure = 0;

void setup(){
  
   
  Serial.begin(BAUDRATE);
   
  initSteppers();

  
  noInterrupts();
  laser_init();  
  interrupts();
  
  laser_on();

  Serial.print("Open Exposer Ready\n");
}

void loop(){
    pressure = analogRead(VAT_PRESSURE_SENSOR);
    Serial.println(pressure);
    processController(); 
    delay(1000);
}




