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
        
          home_y_axis();
          acknowledge();
         
        break;
        
        // home z axis
        case 0x03:

          home_z_axis();
          acknowledge();
       
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
          moveToNextLayer();
          toggle_y_Direction();
          acknowledge();
        break;
        
        case 0x07:
          moveToNextLayer();
          acknowledge();
        break;
        
        case 0x08:
          move_z_to_end_position();
          acknowledge();
        break;
    }

  }
 
  if (exposing_done){
    
                moveToNextLine();
                data_table[0] = 0;
                write_line_enable = 0;
                exposing_done = 0;
                acknowledge();

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

