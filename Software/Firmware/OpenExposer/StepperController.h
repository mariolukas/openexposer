#ifndef STEPPERCONTROLLER_H
#define STEPPERCONTROLLER_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif



void initSteppers();

void moveToNextLine();
void moveToNextLayer();
void move_z_to_end_position();

void motor_enable(int motor);
void motor_disable(int motor);

void toggle_y_Direction();

void home_y_axis();
void home_z_axis();

void move_z_relative();


boolean endStopSwitchReached(int endstop);


#endif
