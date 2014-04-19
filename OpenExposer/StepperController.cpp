#include "configuration.h"
#include "StepperController.h"
#include "AccelStepper.h"

AccelStepper y_stepper(1, Y_STEP, Y_DIR);
AccelStepper z_stepper(2, Z_STEP, Z_DIR);


int y_step_direction = 1;
int z_step_direction = 1;

void initSteppers(){
  
  pinMode(MICROSTEP,OUTPUT); 
  digitalWrite(MICROSTEP, HIGH); //no microstepping
 
  
  y_stepper.setMaxSpeed(MAX_Y_SPEED);
  y_stepper.setAcceleration(MAX_Y_ACCELERATION);
  
  z_stepper.setMaxSpeed(MAX_Z_SPEED);
  z_stepper.setAcceleration(MAX_Z_ACCELERATION);
  

 
  pinMode(Y_ENABLE, OUTPUT);
  digitalWrite(Y_ENABLE, LOW);
  
  pinMode(Z_ENABLE, OUTPUT);
  digitalWrite(Z_ENABLE, LOW);
  
  // ENDSTOP SETTINGS
  pinMode(Y_ENDSTOP, INPUT);
  digitalWrite(Y_ENDSTOP, HIGH);  
  
  pinMode(Z_ENDSTOP, INPUT);
  digitalWrite(Z_ENDSTOP, HIGH); 


}

void toggle_y_Direction(){
    y_step_direction *= -1;
}

void moveToNextLayer(){
   int steps_to_move = LAYER_HEIGHT*Z_STEPS_PER_MM * z_step_direction;
   z_stepper.runToNewPosition(z_stepper.targetPosition()-steps_to_move);
}

void moveToNextLine(){
   int steps_to_move = LINE_WIDTH*Y_STEPS_PER_MM * y_step_direction;
   y_stepper.runToNewPosition(y_stepper.targetPosition()-steps_to_move);
}

void home_z_axis(){
  
    while(endStopSwitchReached(Z_ENDSTOP)){
        z_stepper.runToNewPosition(z_stepper.targetPosition()-100);
    }
    z_stepper.runToNewPosition(z_stepper.targetPosition()+1000);
    z_stepper.setCurrentPosition(0.0);
  
}

void home_y_axis(){
    while(endStopSwitchReached(Y_ENDSTOP)){
       y_stepper.runToNewPosition(y_stepper.targetPosition()+10);
    }
    y_stepper.runToNewPosition(y_stepper.targetPosition()-100);
    y_stepper.setCurrentPosition(0.0);
   
}

boolean endStopSwitchReached(int endstop){
  if(digitalRead(endstop) == LOW){
      return true;
  }
  else 
     return false; 
}


