/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the Uno and
  Leonardo, it is attached to digital pin 13. If you're unsure what
  pin the on-board LED is connected to on your Arduino model, check
  the documentation at http://www.arduino.cc

  This example code is in the public domain.

  modified 8 May 2014
  by Scott Fitzgerald
 */

#define XTAL 8000000L
#define CLOCK 333
#define PRESCALER 1


// the setup function runs once when you press reset or power the board
void setup() {
    pinMode(OUTPUT, PA1);
    pinMode(OUTPUT, 11);
    pinMode(OUTPUT, PB2);
    digitalWrite(11, HIGH);
//    digitalWrite(PB2, HIGH);
    CCP=0xd8;
    CLKPR=(0<<CLKPS3) | (0<<CLKPS2) | (0<<CLKPS1) | (0<<CLKPS0);
//    DDRA = (1 << PA2);//PA2 pin as an output
/* PA2
    TOCPMSA1 = (1 << TOCC1S0);//TOCC1 linkage
    TOCPMCOE = (1 << TOCC1OE);//Enable PWMs
    ICR1 = (XTAL/PRESCALER/CLOCK) -1;
    OCR1A = (XTAL/PRESCALER/CLOCK) -1;
    TCCR1A = (1 << COM1A1) | (1 << COM1A0) | (0 << WGM13) | (1<< WGM12);
    TCCR1B = (0 << CS12) | (0 << CS11) | (1 << CS10);*/

// PB2
    TOCPMSA1 = (1 << TOCC7S0);//TOCC1 linkage
    TOCPMCOE = (1 << TOCC7OE);//Enable PWMs
    ICR1 = (XTAL/PRESCALER/CLOCK) -1;
    OCR1A = (XTAL/PRESCALER/CLOCK) -1;
    TCCR1A = (1 << COM1A1) | (1 << COM1A0) | (0 << WGM13) | (1<< WGM12);
    TCCR1B = (0 << CS12) | (0 << CS11) | (1 << CS10);

}

// the loop function runs over and over again forever
void loop() {

}
