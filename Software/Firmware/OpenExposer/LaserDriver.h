#ifndef LASERDRIVER_H
#define LASERDRIVER_H
#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif


extern uint8_t exposing_done;

void init_laser_driver();
void laser_on();
void laser_off();
void expose_line(int time);
void set_exposing_cycles(uint8_t cycles);
void fill_laser_buffer(long distance);
void create_test_pattern();

#endif

