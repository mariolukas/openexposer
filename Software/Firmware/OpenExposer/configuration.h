#ifndef CONFIGURATION_H
#define CONFIGURATION_H
//OC1A


#define BAUDRATE 115200

// Y Stepper Settings
//driver: 1 | 2 | 3  | 4

        //2 | 5 | 11 | A0
        //3 | 6 | 12 | A1
        //4 | 7 | 13 | A2
        
// STEPPER  
#define Y_ENABLE   5  
#define Y_STEP     6  
#define Y_DIR      7

#define Z_ENABLE  2
#define Z_STEP    3
#define Z_DIR     4

#define MAX_Z_ACCELERATION  999999.0
#define MAX_Z_SPEED 9999.0

#define MAX_Y_ACCELERATION  99999999.0
#define MAX_Y_SPEED 999999.0

#define Y_STEPS_PER_MM 80
#define Z_STEPS_PER_MM 4000

#define Y_RESOLUTION 40
#define Z_RESOLUTION 10


#define END_POSITION_OFFSET Z_STEPS_PER_MM*30

#define LAYER_HEIGHT Z_STEPS_PER_MM/Z_RESOLUTION
#define LINE_WIDTH   Y_STEPS_PER_MM/Y_RESOLUTION

#define STEPS_PER_REVOLUTION 200
#define MICROSTEP   A5 

// Laser Thickness or Line Width



// ENDSTOPS
#define Y_ENDSTOP  A4
#define Z_ENDSTOP  A3

// LASER

#define LASER_PIN         9
#define LASER_PORT        B
#define LASER_BIT         1
#define LASER_PWM_PORT    D
#define LASER_PWM_BIT     6
#define LASER_PWM_PIN     6

#define LASER_EXPOSING_CYCLES 40
#define LASER_POINT_SCALER 24

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




