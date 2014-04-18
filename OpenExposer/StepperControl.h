#ifndef STEPPERCONTROL_H
#define STEPPERCONTROL_H

void initSteppers();
void moveToNextLine();
boolean endStopSwitchReached(int endstop);


#endif
