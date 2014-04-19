#include "configuration.h"
#include "LaserDriver.h"
#include "StepperController.h"
#include "ProcessController.h"

boolean data_received = false;
byte received_command = 0;

void acknowledge(){
      Serial.print(1); 
      received_command = 0; 
      data_received = false;
}


void processController(){

  if(data_received){
     
     switch(received_command){
        case 0x01:
             write_line_enable = 1;
        break;
        
        // home y axis
        case 0x02:
          laser_off();
          home_y_axis();
          acknowledge();
          laser_on();
        break;
        
        // home z axis
        case 0x03:
          laser_off();
          home_z_axis();
          acknowledge();
          laser_on();
        break;
        
        // turn laser on
        case 0x04: 
          laser_on();
          acknowledge();
        break;
        
        // turn laser off
        case 0x05:
         laser_off();
         acknowledge();
        break;
        
        // next layer
        case 0x06:
          // moveToNextLayer here!
          toggle_y_Direction();
          acknowledge();
        break;
    }

  }
 
  if (exposing_done){
                moveToNextLine();
               
                acknowledge();
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
    uint16_t value;
    uint16_t i = 0;

   if( Serial.available() > 0 ) {
       received_command = Serial.read();
       len = getPackage();
       while(i<len){
         value = getPackage();
         data_table[i] = value * LASER_POINT_SCALER;
         i++;
       }
    } 
 
    len = 0;
    i = 0;
    data_received = true;

}

