#define XTAL 8000000L
#define CLOCK 333
// depends on individual attiny 841 
#define CLOCK_OFFSET 10
#define PRESCALER 1
#define DUTY_CYCLE 10000

#define PWM_OUTPUT_PIN 8

void setup() {
  
  pinMode(PWM_OUTPUT_PIN, OUTPUT);

  CCP = 0xd8;
  CLKPR = (0 << CLKPS3) | (0 << CLKPS2) | (0 << CLKPS1) | (0 << CLKPS0);

  TOCPMSA0 = (1 << TOCC1S0);//TOCC1 linkage
  TOCPMCOE = (1 << TOCC1OE);//Enable PWMs

  TCCR1A = (1 << COM1A1) | (0 << COM1A0) | (1 << WGM11) | (0 << WGM10);
  TCCR1B = (1 << CS10) | (1 << WGM13) | (1 << WGM12);

  ICR1 = (XTAL / PRESCALER / (CLOCK - CLOCK_OFFSET));
  OCR1A = DUTY_CYCLE;


}

void loop() {

}
