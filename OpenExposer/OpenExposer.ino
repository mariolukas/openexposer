#include "configuration.h"
#include "LaserDriver.h"
#include "StepperControl.h"
#include "ProcessCommand.h"

const uint8_t DATA_SCALE_VALUE = 28;
boolean data_received = false;


uint16_t i = 100;
byte command = 0;
float pos = 0;

  

void setup(){
  
  Serial.begin(57600);

  initSteppers();


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
      
      moveToNextLine();

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

