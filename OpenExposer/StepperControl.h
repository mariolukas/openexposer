#ifndef STEPPERCONTROL_H
#define STEPPERCONTROL_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif


void initSteppers();
void moveToNextLine();
boolean endStopSwitchReached(int endstop);


#endif
