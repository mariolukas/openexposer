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

#include "LaserDriver.h"

#include "LaserTimer.h"


laser_buffer_type laser_buffer;

static_assert(LASER_POSITIONS_BUFFER_SIZE <= 255, "Maximum buffer size given by type uint8_t (must be <= 255).");

uint16_t begin_delay = 5800;
uint16_t end_delay = 47500ul;
uint16_t sync_timeout_delay = 60000ul;

long laser_timing_scale_dividend = LASER_TIMING_SCALE_DIVIDEND;
long laser_timing_scale_divisor = LASER_TIMING_SCALE_DIVISOR;
uint16_t laser_timing_center_offset = LASER_TIMING_CENTER_OFFSET;


enum class LaserState : uint8_t { WAITING_FOR_SYNC, READY_FOR_LINE };

static LaserState laser_state;
static uint16_t last_line_start;

uint16_t exposing_cycles = 5;
uint16_t exposed_cycles = 0;
volatile uint8_t exposing = 0;

LaserTimer laserTimer;

// Opto Capture ISR
ISR(TIMER1_CAPT_vect){
	last_line_start = laserTimer.getInputCaptureTime();         // save current counter value
//	last_line_start = ICR1;         // save current counter value

	laserTimer.forceClearPinOnMatch();
	//TCCR1A = (1<<COM1A1) ;                //turn off output on compare match
	//TCCR1A = (1<<COM1A1) | (1<<FOC1A);    //Force compare match (Laser off)

	// Input Capture ausschalten
	laserTimer.disableInputCapture();
	//TIMSK1 &= ~(1<<ICIE1); //turn ourselves off

	uint16_t start_time = last_line_start + begin_delay;   //calculate at which timer value to begin lasering
	//uint16_t start_time = ICR1 + begin_delay;   //calculate at which timer value to begin lasering
	laserTimer.setOutputCompareRegisterA(start_time);
	//OCR1A = start_time;                         //set OCR1A to that value (this is used from laser write line)
	laserTimer.setOutputCompareRegisterB(start_time - 500);
	//OCR1B = start_time - 500;            //set up OCR1B to occur long enough before that to have the interrupt

										 //routine ready and waiting for the OCR1A match
	laser_state = LaserState::READY_FOR_LINE;
}

void laser_write_line(){

	uint16_t * timings = laser_buffer.laser_timings;

	//wait for OCR0A compare match (begin of line, laser off)
	laserTimer.waitForCompareRegisterAMatch();
	//while((TIFR1 & (1<<OCF1A)) == 0);
	//TIFR1 = (1<<OCF1A);

	laserTimer.toggleOnCompareMatch();
	//TCCR1A = (1<<COM1A0); //Toggle  laser on compare match from now

	do {
		laserTimer.waitForCompareRegisterAMatch();
		//while ((TIFR1 & (1 << OCF1A)) == 0);  //and wait for it...
		//TIFR1 = (1 << OCF1A);

		uint16_t tmp = *timings++;

		if (tmp == 0) {               //end mark?
			break;                    //yes: end line
		}
		laserTimer.addToOutputCompareRegisterA(tmp);
		//OCR1A += tmp;                   //no: delay that amount
	} while(1);
}

ISR(TIMER1_COMPB_vect){
	if(laser_state == LaserState::READY_FOR_LINE){

		TCCR1A = (1<<COM1A1) | (1<<FOC1A);
	
		if(exposing){
			laser_write_line();
			++exposed_cycles;
		} else {
			laserTimer.waitForCompareRegisterAMatch();
		   	//while((TIFR1 & (1<<OCF1A)) == 0);
	   		//TIFR1 = (1<<OCF1A);

			laserTimer.waitForCompareRegisterAMatch();
			//while((TIFR1 & (1<<OCF1A)) == 0);
			//TIFR1 = (1<<OCF1A);
		}

		if(exposed_cycles == exposing_cycles){
			exposing = 0;
		}

		laserTimer.forceClearPinOnMatch();
		//TCCR1A = (1<<COM1A1) ;
	    //TCCR1A = (1<<COM1A1) | (1<<FOC1A); //Assure that laser is off

		laserTimer.clearInputCaptureFlag();
	    //TIFR1  =  (1<<ICF1); //clear flag
		laserTimer.enableInputCapture();
	    //TIMSK1 |= (1<<ICIE1);  //turn on opto capture int

		laserTimer.setOnCompareMatch();
	    //TCCR1A = (1<<COM1A1) | (1<<COM1A0); //turn laser on on next compare
											//for the sync pulse that hits the opto

		laserTimer.setOutputCompareRegisterA(last_line_start + end_delay);
	    //OCR1A = last_line_start + end_delay;           //set up the time for the sync pulse
	    laser_state = LaserState::WAITING_FOR_SYNC;              //tell ourselves that we are in "searching for sync" state
		laserTimer.setOutputCompareRegisterB(last_line_start + sync_timeout_delay);
		//OCR1B = last_line_start + sync_timeout_delay;  //set up a timeout for the sync pulse to occur
											//(which brings us back in to the interrupt handler to the
											//case below, because the ICR interrupt has not occured
											//and set the laser_state to LS_LINE, and reprogrammed the comnpares)


	} else {

	    // WAITING_FOR_SYNC (we have missed the sync pulse)
		laserTimer.forceClearPinOnMatch();
	    //TCCR1A = (1<<COM1A1) ;
	    //TCCR1A = (1<<COM1A1) | (1<<FOC1A); //Assure that laser is off

		laserTimer.clearInputCaptureFlag();
	    //TIFR1  =  (1<<ICF1); //clear flag
		laserTimer.enableInputCapture();
	    //TIMSK1 |= (1<<ICIE1);  //turn on opto capture int
		laserTimer.setOnCompareMatch();
		//TCCR1A = (1<<COM1A1) | (1<<COM1A0); //turn laser on on next compare (sync)

		laserTimer.setOutputCompareRegisterA(laserTimer.getOutputCompareRegisterB() + end_delay);
		//OCR1A = OCR1B + end_delay;
		laserTimer.setOutputCompareRegisterB(laserTimer.getOutputCompareRegisterB() + sync_timeout_delay);
	    //OCR1B = OCR1B + sync_timeout_delay;

	}
}

// fill data table with test pattern
void create_test_pattern(){

	for(int i=0; i < 80; ++i){
		laser_buffer.laser_timings[i] = 500-i;
	}
	laser_buffer.laser_timings[81] = 0;
    laser_buffer.length = 0;
}

void expose_line(uint16_t cycles) {
	exposing_cycles = cycles;
	exposed_cycles = 0;

	exposing = 1;
   
	while(exposing);
}

// initialize laser 
void init_laser_driver(){
  
	create_test_pattern();

	SET_DDR(LASER);

	SET_DDR(LASER_PWM);
	OUTPUT_ON(LASER_PWM);

	laserTimer.startTimer();
	//TCCR1B = 1;
}

void fill_laser_buffer(long distance){
	if (distance == 0) {
		laser_buffer.positions[laser_buffer.length] = 0;
		convert_positions_to_timings();
        laser_buffer.length = 0;
	} else {
		laser_buffer.positions[laser_buffer.length] = distance;
        ++laser_buffer.length;
	}
//    delay(1);
}

void convert_positions_to_timings() {
	long current_position = 0;
	for(int i = 0; i < laser_buffer.length; ++i) {
		current_position += laser_buffer.positions[i];
		laser_buffer.laser_timings[i] = current_position * laser_timing_scale_dividend / laser_timing_scale_divisor + laser_timing_center_offset;
	}
	laser_buffer.laser_timings[laser_buffer.length] = 0;
}

// Turn Laser Timer on and activate Opto Capture
void laser_on(){

	laserTimer.setValue(1);
	//TCNT1 = 1;

	laserTimer.setOutputCompareRegisterB(0);
	//OCR1B = 0;
	laserTimer.setOutputCompareRegisterA(0);
	//OCR1A = 0;

	laserTimer.clearInputCaptureAndOutputCompareBFlag();
	//TIFR1 = (1<<OCF1B) | (1<<ICF1);
	laserTimer.enableInputCaptureAndOutputCompareBInterrupt();
	//TIMSK1 |= (1<<OCIE1B) | (1<<ICIE1); //capture b and icp int on (they do all the work)
}

// Turn Laser Timer off and deactivate laser opto
void laser_off(){

	laserTimer.disableInputCaptureAndOutputCompareBInterrupt();
	//TIMSK1 &= ~ ((1<<OCIE1B) | (1<<ICIE1)); //ints off
	laserTimer.disableTimerPin();
	//TCCR1A = 0; //disconnect laser from timer
}
