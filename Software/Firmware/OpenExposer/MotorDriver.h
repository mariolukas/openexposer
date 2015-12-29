#ifndef STEPPERCONTROLLER_H
#define STEPPERCONTROLLER_H

#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

// Helper Macro degrees to Microseconds for Timer2 Servo
#define degreesToMS( _degrees) (_degrees * 6 + 900)

void init_motor_driver();
void motors_release();
void do_move(float x_distcance, float y_distance, float feedrate);
void home_z_axis();
void home_y_axis();
void vat_down();
void vat_up();


#endif
