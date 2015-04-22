#ifndef STEPPERCONTROLLER_H
#define STEPPERCONTROLLER_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

void init_motor_driver();
void motors_release();
void do_move(float x_distcance, float y_distance, float feedrate);
void home_z_axis();
void home_y_axis();


#endif
