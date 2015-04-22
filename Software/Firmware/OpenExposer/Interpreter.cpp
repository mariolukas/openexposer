#include "configuration.h"
#include "LaserDriver.h"
#include "MotorDriver.h"
#include "Interpreter.h"

char buffer[MAX_SERIAL_BUFFER];  // where we store the message until we get a ';'
int sofar;  // how much is in the buffer

// settings
char mode_abs=1;  // absolute mode??
long line_number=0;


/**
 * Look for character /code/ in the buffer and read the float that immediately follows it.
 * @return the value found.  If nothing is found, /val/ is returned.
 * @input code the character to look for.
 * @input val the return value if /code/ is not found.
 **/
long parsedistance(char code,long val) {
  char *ptr=buffer;
  while(ptr && *ptr && ptr<buffer+sofar) {
    if(*ptr==code) {
      return atol(ptr+1);
    }
    ptr=strchr(ptr,' ')+1;
  }
  return val;
} 

float parsenumber(char code,float val) {
  char *ptr=buffer;
  while(ptr && *ptr && ptr<buffer+sofar) {
    if(*ptr==code) {
      return atof(ptr+1);
    }
    ptr=strchr(ptr,' ')+1;
  }
  return val;
} 
/**
 * prepares the input buffer to receive a new message and tells the serial connected device it is ready for more.
 */
void ready() {
  sofar=0;  // clear input buffer
  Serial.print(F(">"));  // signal ready to receive input
}


/**
 * display helpful information
 */
void help() {
  Serial.print(F("Open Exposer Firmware "));
  Serial.println(VERSION);
  Serial.println(F("Commands:"));
  Serial.println(F("G00 [Y(10/mm)] [Z(10/mm)] [F(feedrate)]; - linear move"));
  Serial.println(F("G01 [Y(10/mm)] [Z(10/mm)] [F(feedrate)]; - linear move"));
  Serial.println(F("G04 E[cycles]; - exposing cycles"));
  Serial.println(F("G05 D[distance] - distance value in line (last value must be 0)"));
  Serial.println(F("G90; - absolute mode"));
  Serial.println(F("G91; - relative mode"));
  Serial.println(F("G92 [Y(steps)] [Z(steps)]; - change logical position"));
  Serial.println(F("M18; - disable motors"));
  Serial.println(F("M21; - start expose line in buffer"));
  Serial.println(F("M19; - laser on"));
  Serial.println(F("M20; - laser off")); 
  Serial.println(F("M100; - this help message"));
  Serial.println(F("M114; - report position and feedrate"));
}


/**
 * Read the input buffer and find any recognized commands.  One G or M command per line.
 */
void processCommand() {
  // blank lines
  if(buffer[0]==';') return;
  
  long cmd;

  // is there a line number?
  cmd=parsenumber('N',-1);
  if(cmd!=-1 && buffer[0]=='N') {  // line number must appear first on the line
    if( cmd != line_number ) {
      // wrong line number error
      Serial.print(F("BADLINENUM "));
      Serial.println(line_number);
      return;
    }
  
    // is there a checksum?
    if(strchr(buffer,'*')!=0) {
      // yes.  is it valid?
      char checksum=0;
      int c=0;
      while(buffer[c]!='*') checksum ^= buffer[c++];
      c++; // skip *
      int against = strtod(buffer+c,NULL);
      if( checksum != against ) {
        Serial.print(F("BADCHECKSUM "));
        Serial.println(line_number);
        return;
      } 
    } else {
      Serial.print(F("NOCHECKSUM "));
      Serial.println(line_number);
      return;
    }
    
    line_number++;
  }

  cmd = parsenumber('G',-1);
  switch(cmd) {
  case  0: // move linear
  case  1: // move linear
      // Move Linear here
      do_move(parsenumber('Y',0), parsenumber('Z',0), parsenumber('F',30000));
    break;
  case 3:
     delay(parsenumber('D',0));
  break;
  case  4:  
      set_exposing_cycles(parsenumber('E',0));
    break;  // dwell
  case 5:
      fill_laser_buffer(parsedistance('D',0));
    break;
  case 6:
      delay(20);
      expose_line(parsenumber('E',1000));
    break;
  case 7:
       create_test_pattern();
       expose_line(parsenumber('E',1000));
     break;  
  case 29:
      //home z- axis
     home_z_axis();
     break;
  case 30:
     home_y_axis();
     break;
   
  case 28:
      // home all axis
      break;  
  
  case 90:  mode_abs=1;  break;  // absolute mode
  case 91:  mode_abs=0;  break;  // relative mode
  case 92:  // set logical position
      // set position to 0 here
    break;
  default:  break;
  }
  
  // M Code section 
  cmd = parsenumber('M',-1);
  switch(cmd) {
  case 18:  // disable motors
    motors_release();
    break;
  case 19:
     laser_on(); 
    break;
  case 20:
     laser_off();
    break;
  case 100:  help();  break;
  case 110:  line_number = parsenumber('N',line_number);  break;
  case 114:  
    // print position here  
  break;
  default:  break;
  }
}








