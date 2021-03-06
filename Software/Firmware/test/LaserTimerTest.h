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

#ifndef OPENEXPOSER_TESTLASERTIMER_H
#define OPENEXPOSER_TESTLASERTIMER_H

#include "gtest/gtest.h"

#include "OpenExposer/LaserTimer.h"

class LaserTimerTest : public ::testing::Test
{
protected:
    LaserTimer laserTimer;

    virtual void SetUp()
    {
    }

    virtual void TearDown()
    {
    }
};

#endif //OPENEXPOSER_TESTLASERTIMER_H
