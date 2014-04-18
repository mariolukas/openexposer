#ifndef CONFIGURATION_H
#define CONFIGURATION_H
//OC1A


// Y Stepper Settings
//driver: 1 | 2 | 3  | 4
        //2 | 5 | 11 | A0
        //3 | 6 | 12 | A1
        //4 | 7 | 13 | A2
        
// STEPPER  
#define Y_ENABLE   5  
#define Y_STEP     6  
#define Y_DIR      7

#define Z_ENABLE   2
#define Z_STEP     3
#define Z_DIR      4

#define STEPS_PER_REVOLUTION 200
#define MICROSTEP   A5 

// Laser Thickness or Line Width
#define LINE_WIDTH 5


// ENDSTOPS
#define Y_ENDSTOP  A4
#define Z_ENDSTOP  A3

// LASER

#define LASER_PIN 9
#define LASER_PORT        B
#define LASER_BIT         1
#define LASER_PWM_PORT    D
#define LASER_PWM_BIT     6
#define LASER_PWM_PIN 6


// OPTO

#define OPTO_PIN 8


// USEFUL MACROS

#define PORT_(port) PORT ## port 
#define DDR_(port)  DDR  ## port 
#define PIN_(port)  PIN  ## port 

#define PORT(port) PORT_(port) 
#define DDR(port)  DDR_(port) 
#define PIN(port)  PIN_(port)

#define SET_DDR(p)    DDR(p##_PORT) |= (1<<p##_BIT)
#define CLEAR_DDR(p)  DDR(p##_PORT) &= ~(1<<p##_BIT)
#define OUTPUT_ON(p)  PORT(p##_PORT) |= (1<<p##_BIT)
#define OUTPUT_OFF(p) PORT(p##_PORT) &= ~(1<<p##_BIT)
#define _INPUT(p)    ((PIN(p##_PORT) & (1<<p##_BIT)) != 0)

#endif




