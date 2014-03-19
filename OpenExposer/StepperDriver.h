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

// ensure this library description is only included once
#ifndef StepperDriver_h
#define StepperDriver_h

// library interface description
class StepperDriver {
  public:
    // constructors:
    StepperDriver();
    void setStep(int number_of_steps, int dir_pin, int step_pin);

    // speed setter method:
    void setSpeed(long whatSpeed);

    // mover method:
    void step(long number_of_steps);
    //update method:
    int update();
    int version(void);

  private:
    void stepMotor(int thisDir);
    void determineDirection(long number_of_steps);
    void setAction(long number_of_steps);
    void maybeStepMotor(long* steps_left_ptr);
    int done;
    bool running;
    int direction;        // Direction of rotation
    int speed;          // Speed in RPMs
    unsigned long step_delay;    // delay between steps, in ms, based on speed
    int number_of_steps;      // total number of steps this motor can take
    long step_number;        // which step the motor is on
    long seq_steps_left;   //number of steps left if running a sequence
    
    // motor pin numbers:
    int dir_pin;
    int step_pin;
    
    long last_step_time;      // time stamp in ms of when the last step was taken
};

#endif

