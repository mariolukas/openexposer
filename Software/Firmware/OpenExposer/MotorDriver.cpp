/**
 * OpenExposer firmware
 *
 *  Copyright 2014 by Mario Lukas <info@mariolukas.de>
 *
 * This file is part of OpenExposer firmware.
 *
 * OpenExposer firmware is free software: you can redistribute
 * it and/or modify it under the terms of the GNU General Public
 * License as published by the Free Software Foundation, either
 * version 3 of the License, or (at your option) any later version.
 *
 * OpenExposer firmware is distributed in the hope that it will
 * be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 * of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
 *
 * @license GPL-3.0+ <http://opensource.org/licenses/GPL-3.0>
 */

#include "MotorDriver.h"

#include "configuration.h"
#include "AccelStepper.h"


AccelStepper y(1, Y_STEP_PIN, Y_DIR_PIN);
AccelStepper z(2, Z_STEP_PIN, Z_DIR_PIN);
//ServoTimer2 vat_servo;

void vat_down(){

 // vat_servo.attach(VAT_SERVO_PIN); 
  
  for(int pos=SERVO_MAX_POS; pos > SERVO_MIN_POS; pos--){
      
      //vat_servo.write(degreesToMS(pos));
      delay(10);
  }; 
 
}

void vat_up(){

  for(int pos=SERVO_MIN_POS; pos < SERVO_MAX_POS; pos++){
     // vat_servo.write(degreesToMS(pos));
      delay(10);
  }; 
 // vat_servo.detach(); 


}



void motors_release(){
  digitalWrite(Z_ENABLE_PIN, HIGH);
  digitalWrite(Y_ENABLE_PIN, HIGH);
}

void motors_enable(){
    digitalWrite(Z_ENABLE_PIN, LOW);
    digitalWrite(Y_ENABLE_PIN, LOW);
}


void enable_y_motor(){
  digitalWrite(Y_ENABLE_PIN, LOW);
}

void enable_z_motor(){
  digitalWrite(Z_ENABLE_PIN, LOW);
}

void release_y_motor(){
 digitalWrite(Y_ENABLE_PIN, HIGH);
}

void release_z_motor(){
 digitalWrite(Z_ENABLE_PIN, HIGH);
}

uint8_t direction(long distance){
    if (distance < 0) {
        return HIGH;
    } else {
        return LOW;
    }
}


void step(AccelStepper motor, float steps, float speed_value, float){
      
      motor.moveTo(motor.currentPosition()+steps);
      motor.setSpeed(speed_value);
      //motor.setAcceleration(acceleration);
      
      // Implementation without acceleration.
      while (motor.distanceToGo() != 0)
        motor.runSpeedToPosition();
        //motor.run();
     
}


void do_move(float y_distance, float z_distance, float feedrate){

  
    float y_speed = feedrate;
    float z_speed = feedrate;
    float y_acceleration = 200;
    float z_acceleration = 600;
    
    if(y_distance != 0){
      
      enable_y_motor();
      step(y, y_distance*Y_STEPS_PER_MM, y_speed, y_acceleration);
      //motors_release();
      //release_y_motor();
    }
    
    if(z_distance != 0){
      enable_z_motor();
      //motors_enable();
      step(z, z_distance*Z_STEPS_PER_MM, z_speed, z_acceleration);
      //release_z_motor();
      //motors_release();
    }

 
}


void init_motor_driver(){
    pinMode(MICROSTEP,OUTPUT);
    

    
    pinMode(Z_ENABLE_PIN, OUTPUT);
    pinMode(Y_ENABLE_PIN, OUTPUT);
    
    motors_release();
    z.setMaxSpeed(200000.0);
    z.setSpeed(10000.0); 
    y.setMaxSpeed( 100000.0);
    y.setSpeed(1000.0); 
    
    // Endstops
    pinMode(Y_ENDSTOP, INPUT);
    digitalWrite(Y_ENDSTOP, HIGH); 
    motors_enable();

}


boolean endStopSwitchReached(int endstop){
  if(digitalRead(endstop) == HIGH){
      return false;
  }
  else 
     return true; 
}

void home_y_axis(){
  
     motors_enable(); 
     while(!endStopSwitchReached(Y_ENDSTOP)){
       step(y, 100, 10000, 10000);
     }
     y.setCurrentPosition(0.0);
     y.setSpeed(10000.0); 
     motors_release();

}

void home_z_axis(){

    motors_enable(); 
     while(!endStopSwitchReached(Z_ENDSTOP)){
       step(z, 10, 80000, 10000);
     }
    
    z.setCurrentPosition(0.0);

    z.setSpeed(30000.0); 
    motors_release();
    
}

