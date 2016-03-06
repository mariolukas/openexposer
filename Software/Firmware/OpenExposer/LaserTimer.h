/**
 * OpenExposer firmware
 *
 *  Copyright 2016 by Christoph Emonds <info@christoph-emonds.de>
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

#ifndef OPENEXPOSER_LASERTIMER_H
#define OPENEXPOSER_LASERTIMER_H

#include <avr/io.h>

class LaserTimer
{

public:
    void startTimer();
    void setValue(uint16_t value);
    void disableTimerPin();
    void forceClearPinOnMatch();
    void setOnCompareMatch();
    void toggleOnCompareMatch();
    void enableInputCapture();
    void disableInputCapture();
    void clearInputCaptureFlag();
    void clearInputCaptureAndOutputCompareBFlag();
    uint16_t getInputCaptureTime();
    void enableInputCaptureAndOutputCompareBInterrupt();
    void disableInputCaptureAndOutputCompareBInterrupt();
    void setOutputCompareRegisterA(uint16_t value);
    uint16_t getOutputCompareRegisterA();
    void addToOutputCompareRegisterA(uint16_t value);
    void setOutputCompareRegisterB(uint16_t value);
    uint16_t getOutputCompareRegisterB();
    void waitForCompareRegisterAMatch();
};

inline void LaserTimer::startTimer()
{
    TCCR1B = 1;
}

inline void LaserTimer::setValue(uint16_t value)
{
    TCNT1 = value;
}

inline void LaserTimer::disableTimerPin()
{
    TCCR1A = 0;
}

inline void LaserTimer::forceClearPinOnMatch()
{
    TCCR1A = (1<<COM1A1);
    TCCR1A = (1<<COM1A1) | (1<<FOC1A);
}

inline void LaserTimer::setOnCompareMatch()
{
    TCCR1A = (1<<COM1A1) | (1<<COM1A0);
}

inline void LaserTimer::toggleOnCompareMatch()
{
    TCCR1A = (1<<COM1A0);
}

inline void LaserTimer::disableInputCapture()
{
    TIMSK1 &= ~(1<<ICIE1);
}

inline void LaserTimer::enableInputCapture()
{
    TIMSK1 |= (1<<ICIE1);
}

inline void LaserTimer::clearInputCaptureFlag()
{
    TIFR1 = (1<<ICF1);
}

inline void LaserTimer::clearInputCaptureAndOutputCompareBFlag()
{
    TIFR1 = (1<<OCF1B) | (1<<ICF1);
}

inline uint16_t LaserTimer::getInputCaptureTime()
{
    return ICR1;
}

inline void LaserTimer::enableInputCaptureAndOutputCompareBInterrupt()
{
    TIMSK1 |= (1<<OCIE1B) | (1<<ICIE1);
}

inline void LaserTimer::disableInputCaptureAndOutputCompareBInterrupt()
{
    TIMSK1 &= ~ ((1<<OCIE1B) | (1<<ICIE1));
}

inline void LaserTimer::setOutputCompareRegisterA(uint16_t value)
{
    OCR1A = value;
}

inline uint16_t LaserTimer::getOutputCompareRegisterA()
{
    return OCR1A;
}

inline void LaserTimer::addToOutputCompareRegisterA(uint16_t value)
{
    OCR1A += value;
}

inline void LaserTimer::setOutputCompareRegisterB(uint16_t value)
{
    OCR1B = value;
}

inline uint16_t LaserTimer::getOutputCompareRegisterB()
{
    return OCR1B;
}

inline void LaserTimer::waitForCompareRegisterAMatch()
{
    while ((TIFR1 & (1 << OCF1A)) == 0);  //and wait for compare flag is set
    TIFR1 = (1 << OCF1A); // clear the flag
}




#endif //OPENEXPOSER_LASERTIMER_H
