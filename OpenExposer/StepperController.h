#ifndef STEPPERCONTROLLER_H
#define STEPPERCONTROLLER_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif


void initSteppers();

void moveToNextLine();
void  moveToNextLayer();

void home_y_axis();
void home_z_axis();

boolean endStopSwitchReached(int endstop);


#endif
