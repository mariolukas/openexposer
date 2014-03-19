#include "configuration.h"
#include "LaserDriver.h"
#include "AccelStepper.h"

const uint8_t DATA_SCALE_VALUE = 30;
boolean data_received = false;


uint16_t i = 100;
byte command = 0;
float pos = 0;
AccelStepper stepper(1, Y_STEP, Y_DIR);
  

void setup(){
  
  Serial.begin(57600);
  //y_axis_motor.setSpeed(40);

    stepper.setMaxSpeed(50.0);
    stepper.setAcceleration(500.0);

  /*
 
  pinMode(MICROSTEP,OUTPUT);

  */
  pinMode(MICROSTEP,OUTPUT);
  pinMode(Y_ENABLE, OUTPUT);
 // pinMode(Y_STEP, OUTPUT);
 // pinMode(Y_DIR, OUTPUT);
  

  digitalWrite(MICROSTEP, HIGH); //no microstepping
  digitalWrite(Y_ENABLE, LOW);//activate driver

  //y_axis_motor.speed(5);
  noInterrupts();
  laser_init();  
  interrupts();
  
  Serial.print("Exposer Ready\n");
  laser_on();
}

void loop(){
    
   if(data_received){
     
     switch(command){
        case 0x01:
           write_line_enable = 1;
        break;
     
    }
    
    data_received = false;
  }
  
     

  
   if (exposing_done){
      
      stepper.move(20);
      
      while(stepper.run());
      
      Serial.print(1); 
      write_line_enable = 0;
      exposing_done = 0; 
   }
      
  
}

int getPackage() {
	unsigned int data = 0;
	int chr, i;
	for( i = 0 ; i < 2 ; i++ ) {
		chr = Serial.read();
		if( chr == -1 ) {
			i--;
			continue;
		}

		data += ( chr << (8 * i) );
	}

	return data;
}


void serialEvent(){

    int len;
    byte cmd;
    uint16_t value;
    uint16_t i = 0;

   if( Serial.available() > 0 ) {
       cmd = Serial.read();
      
       len = getPackage();
       while(i<len){
         value = getPackage();
         data_table[i] = value * DATA_SCALE_VALUE;
         i++;
       }
    } 
  
    command = cmd;
 
    len = 0;
    cmd = ' ';
    i = 0;
    data_received = true;

}

