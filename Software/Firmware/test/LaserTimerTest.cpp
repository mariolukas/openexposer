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

#include "LaserTimerTest.h"


TEST_F(LaserTimerTest, startTimer)
{
    TCCR1B = 0;
    laserTimer.startTimer();
    EXPECT_EQ(TCCR1B, 1);
}


TEST_F(LaserTimerTest, setValue)
{
    TCNT1 = 0;
    laserTimer.setValue(12345);
    EXPECT_EQ(TCNT1, 12345);
}

TEST_F(LaserTimerTest, disableTimerPin)
{
    TCCR1A = 1;
    laserTimer.disableTimerPin();
    EXPECT_EQ(TCCR1A, 0);
}

TEST_F(LaserTimerTest, forceClearPinOnMatch)
{
    TCCR1A = 0;
    laserTimer.forceClearPinOnMatch();
    EXPECT_GT(TCCR1A & (1<<COM1A1), 0);
    EXPECT_GT(TCCR1A & (1<<FOC1A), 0);
}

TEST_F(LaserTimerTest, setOnCompareMatch)
{
    TCCR1A = 0;
    laserTimer.setOnCompareMatch();
    EXPECT_GT(TCCR1A & (1<<COM1A1), 0);
    EXPECT_GT(TCCR1A & (1<<COM1A0), 0);
}

TEST_F(LaserTimerTest, toggleOnCompareMatch)
{
    TCCR1A = 0;
    laserTimer.toggleOnCompareMatch();
    EXPECT_GT(TCCR1A & (1<<COM1A0), 0);
}

TEST_F(LaserTimerTest, disableInputCapture)
{
    TIMSK1 = 0xff;
    laserTimer.disableInputCapture();
    EXPECT_EQ(TIMSK1, 0xdf);
}

TEST_F(LaserTimerTest, enableInputCapture)
{
    TIMSK1 = 0;
    laserTimer.enableInputCapture();
    EXPECT_EQ(TIMSK1, 0x20);
}

TEST_F(LaserTimerTest, clearInputCaptureFlag)
{
    TIFR1 = 0;
    laserTimer.clearInputCaptureFlag();
    EXPECT_GT(TIFR1, 1);
}

TEST_F(LaserTimerTest, clearInputCaptureAndOutputCompareBFlag)
{
    TIFR1 = 0;
    laserTimer.clearInputCaptureAndOutputCompareBFlag();
    EXPECT_GT(TIFR1, 1);
}

TEST_F(LaserTimerTest, getInputCaptureTime)
{
    ICR1 = 123;
    EXPECT_EQ(laserTimer.getInputCaptureTime(), 123);
}

TEST_F(LaserTimerTest, enableInputCaptureAndOutputCompareBInterrupt)
{
    TIMSK1 = 0x81;
    laserTimer.enableInputCaptureAndOutputCompareBInterrupt();
    EXPECT_EQ(TIMSK1, 0xa9);
}

TEST_F(LaserTimerTest, disableInputCaptureAndOutputCompareBInterrupt)
{
    TIMSK1 = 0xff;
    laserTimer.disableInputCaptureAndOutputCompareBInterrupt();
    EXPECT_EQ(TIMSK1, 0xd7);
}

TEST_F(LaserTimerTest, setOutputCompareRegisterA)
{
    OCR1A = 1;
    laserTimer.setOutputCompareRegisterA(12345);
    EXPECT_EQ(OCR1A, 12345);
}

TEST_F(LaserTimerTest, getOutputCompareRegisterA)
{
    OCR1A = 1;
    EXPECT_EQ(laserTimer.getOutputCompareRegisterA(), 1);
}

TEST_F(LaserTimerTest, addToOutputCompareRegisterA)
{
    OCR1A = 1;
    laserTimer.addToOutputCompareRegisterA(12345);
    EXPECT_EQ(OCR1A, 12346);
}

TEST_F(LaserTimerTest, setOutputCompareRegisterB)
{
    OCR1B = 1;
    laserTimer.setOutputCompareRegisterB(12345);
    EXPECT_EQ(OCR1B, 12345);
}

TEST_F(LaserTimerTest, getOutputCompareRegisterB)
{
    OCR1B = 1;
    EXPECT_EQ(laserTimer.getOutputCompareRegisterB(), 1);
}

TEST_F(LaserTimerTest, waitForCompareRegisterAMatch)
{
    /*
     * There is no easy way to test for this, since
     * TIFR1 is just a variable, no register with some
     * logic. Therefore just don't do anything.
     */
}
