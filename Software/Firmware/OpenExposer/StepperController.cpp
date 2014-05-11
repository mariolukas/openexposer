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
 
  
  y_stepper.setMaxSpeed((long) MAX_Y_SPEED);
  y_stepper.setAcceleration((long) MAX_Y_ACCELERATION);
  
  z_stepper.setMaxSpeed((long) MAX_Z_SPEED);
  z_stepper.setAcceleration((long) MAX_Z_ACCELERATION);
 
  z_stepper.setSpeed((long) 100000); 
 
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
   long steps_to_move = (long) LAYER_HEIGHT * z_step_direction;
   long steps_flow_control = (long) FLOW_CONTROL_DISTANCE;
   
   
   motor_enable(Z_ENABLE);
   
   z_stepper.move(steps_flow_control);
   z_stepper.runToPosition();
   //z_stepper.runToNewPosition(z_stepper.targetPosition()+steps_flow_control);
   delay(100);
   z_stepper.move(-steps_flow_control+steps_to_move);
   z_stepper.runToPosition();
   //z_stepper.runToNewPosition(z_stepper.targetPosition()-steps_flow_control+steps_to_move);

   motor_disable(Z_ENABLE);
}

void moveToNextLine(){
   int steps_to_move = LINE_WIDTH * y_step_direction;
   y_stepper.runToNewPosition(y_stepper.targetPosition()-steps_to_move);
}

void home_z_axis(){
  
   
  
    while(endStopSwitchReached(Z_ENDSTOP)){
        z_stepper.runToNewPosition(z_stepper.targetPosition()-100);
    }
    z_stepper.runToNewPosition(z_stepper.targetPosition()+1000);
    z_stepper.setCurrentPosition(0.0);
    motor_disable(Z_ENABLE);
  
}

void motor_enable(int motor){
   digitalWrite(motor, LOW);
}

void motor_disable(int motor){
   digitalWrite(motor, HIGH);
}

void move_z_relative(){
     
     long steps_to_move = (long) Z_STEPS_PER_MM * 10;
     motor_enable(Z_ENABLE);
     z_stepper.move(steps_to_move);
     z_stepper.runToPosition();
  
     motor_disable(Z_ENABLE);
}


void home_y_axis(){
    while(endStopSwitchReached(Y_ENDSTOP)){
       y_stepper.runToNewPosition(y_stepper.targetPosition()+10);
    }
    y_stepper.runToNewPosition(y_stepper.targetPosition()-500);
    y_stepper.setCurrentPosition(0.0);
   
}

void move_z_to_end_position(){
     long steps_to_move = (long) END_POSITION_OFFSET;
     motor_enable(Z_ENABLE);
     z_stepper.move(steps_to_move);
     z_stepper.runToPosition();
  
     motor_disable(Z_ENABLE);
    // z_stepper.runToNewPosition(z_stepper.targetPosition()+END_POSITION_OFFSET);
}

boolean endStopSwitchReached(int endstop){
  if(digitalRead(endstop) == LOW){
      return true;
  }
  else 
     return false; 
}


