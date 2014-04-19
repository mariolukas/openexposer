#include "configuration.h"
#include "LaserDriver.h"
#include "StepperController.h"
#include "ProcessController.h"

boolean data_received = false;
byte received_command = 0;


void startExposing(){
   write_line_enable = 1;
}

void postExposingProcess(){
    if (exposing_done){
      
      moveToNextLine();

      Serial.print(0x01); 
      write_line_enable = 0;
      exposing_done = 0; 
   }
}

void processController(){

   if(data_received){
     
     switch(received_command){
        case 0x01:
          startExposing();
        break;
        
        case 0x02:
          home_y_axis();
        break;
        
        case 0x03:
          home_z_axis();
        break;
        
     
    }
    
    data_received = false;
  }
  
  postExposingProcess();
  
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

