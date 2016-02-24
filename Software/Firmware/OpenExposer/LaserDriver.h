#ifndef LASERDRIVER_H
#define LASERDRIVER_H

#include <Arduino.h>

#include "configuration.h"

extern uint8_t exposing_done;

typedef union {
    long positions[LASER_POSITIONS_BUFFER_SIZE];
    uint16_t laser_timings[LASER_POSITIONS_BUFFER_SIZE];
} laser_buffer_type;

void init_laser_driver();
void laser_on();
void laser_off();
void expose_line(int time);
void set_exposing_cycles(uint8_t cycles);
void fill_laser_buffer(int32_t distance);
void create_test_pattern();
void convert_positions_to_timings();

#endif

