/*
 StepperDriver is a modification of Stepper.cpp that adds
 non-blocking capability and is focused on Stepper Motor Drivers using STEP and DIR pins. 
 As long as you call update() often, you don't have to wait for the stepper to complete its movement
 before you can make other function calls. Update also does a return when the steps are complete.
 
 The original stepper.cpp v0.4 notes:
 
 Stepper.h - - Stepper library for Wiring/Arduino - Version 0.4
 
 Original library     (0.1) by Tom Igoe.
 Two-wire modifications   (0.2) by Sebastian Gassner
 Combination version   (0.3) by Tom Igoe and David Mellis
 Bug fix for four-wire   (0.4) by Tom Igoe, bug fix from Noah Shibley
 Non-blocking code by Rob Seward in 2009, it's based off of Stepper.cpp version 0.4
 Alterations for Stepper Driver Boards and no interuption by Chris Coleman 2011

*/


#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

#include "StepperDriver.h"

/*
 * Allows you to initiate an array of generic stepper motors in the setup and configure on the fly
 */
StepperDriver::StepperDriver()
{
  this->step_number = 0L;      // which step the motor is on
  this->speed = 0;        // the motor speed, in revolutions per minute
  this->direction = 0;      // motor direction
  this->last_step_time = 0;    // time stamp in ms of the last step taken
  this->number_of_steps = 0;    // total number of steps for this motor
  this->dir_pin = 0;
  this->step_pin = 0;
  this->done = 0;
  this->running = false;
}


/*
 *   setup the stepper pins
 *   
 */
void StepperDriver::setStep(int number_of_steps, int dir_pin, int step_pin){
this->number_of_steps = number_of_steps;    // total number of steps for this motor
  
  // Arduino pins for the motor control connection:
  this->dir_pin = dir_pin;
  this->step_pin = step_pin;

  // setup the pins on the microcontroller:
  pinMode(this->dir_pin, OUTPUT);
  pinMode(this->step_pin, OUTPUT);

}
/*
  Sets the speed in revs per minute

*/
void StepperDriver::setSpeed(long whatSpeed)
{
  this->step_delay = 60L * 1000000L / this->number_of_steps / whatSpeed;
}

/*
  Moves the motor steps_to_move steps.  If the number is negative, 
   the motor moves in the reverse direction.
 */
void StepperDriver::step(long steps_to_move)
{  
  long steps_left ;  // how many steps to take
    setAction(steps_to_move);
    
}

void StepperDriver::setAction(long steps_to_move){
  this->seq_steps_left = abs(steps_to_move);  // how many steps to take
  determineDirection(steps_to_move);
}

void StepperDriver::determineDirection(long steps_to_move){
	// determine direction based on whether steps_to_mode is + or -:
  if (steps_to_move > 0) {this->direction = 1;}
  if (steps_to_move < 0) {this->direction = 0;}
  
}

int StepperDriver::update(){
    done = 0;
	if(this->seq_steps_left > 0) {
		maybeStepMotor(&this->seq_steps_left);
        running = true;
	}else{
        if(this->seq_steps_left == 0 && running){
            done = 1;
        }
        running = false;
    }
    return done;
}

void StepperDriver::maybeStepMotor(long *steps_left_ptr){
	if (micros() - this->last_step_time >= this->step_delay) {
      // get the timeStamp of when you stepped:
      this->last_step_time = micros();
      *steps_left_ptr = *steps_left_ptr - 1L;
      // step the motor to step number 0, 1, 2, or 3:
      stepMotor(this->direction);
  }	
}

/*
 * Moves the motor forward or backwards.
 */
void StepperDriver::stepMotor(int thisDir)
{
      digitalWrite(dir_pin, thisDir);
	  delayMicroseconds(100);
	  digitalWrite(step_pin, LOW);
          delayMicroseconds(100);
	  digitalWrite(step_pin, HIGH);
	  delayMicroseconds(100);
 }


/*
  version() returns the version of the library:
*/
int StepperDriver::version(void)
{
  return 5;
}
