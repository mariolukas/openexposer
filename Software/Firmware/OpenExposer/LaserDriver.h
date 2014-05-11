#ifndef LASERDRIVER_H
#define LASERDRIVER_H
#if ARDUINO >= 100
#include "Arduino.h"
#else
#include "WProgram.h"
#endif

extern uint16_t offset;
extern uint16_t data_table[512];
extern volatile uint8_t write_line_enable;
extern uint8_t exposing_done;

void laser_init();
void laser_on();
void laser_off();
void laser_write_line();
void exposeLine();
void set_exposing_cycles();

#endif

