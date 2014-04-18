#include "configuration.h"
#include "StepperControl.h"
#include "AccelStepper.h"

AccelStepper y_stepper(1, Y_STEP, Y_DIR);
AccelStepper z_stepper(2, Z_STEP, Z_DIR);

void initSteppers(){
  
  pinMode(MICROSTEP,OUTPUT); 
  digitalWrite(MICROSTEP, HIGH); //no microstepping
 
  
  y_stepper.setMaxSpeed(14550.0);
  y_stepper.setAcceleration(12500.0);
  
  z_stepper.setMaxSpeed(14550.0);
  z_stepper.setAcceleration(12500.0);
  
  pinMode(Y_ENABLE, OUTPUT);
  digitalWrite(Y_ENABLE, LOW);
  
  pinMode(Z_ENABLE, OUTPUT);
  digitalWrite(Z_ENABLE, LOW);
  
}

void moveToNextLine(){
   int steps_to_move = LINE_WIDTH;
   y_stepper.runToNewPosition(y_stepper.targetPosition()-steps_to_move);
}


