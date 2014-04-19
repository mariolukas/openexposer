#ifndef STEPPERCONTROLLER_H
#define STEPPERCONTROLLER_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif


void initSteppers();
void moveToNextLine();
void home_y_axis();
boolean endStopSwitchReached(int endstop);


#endif
