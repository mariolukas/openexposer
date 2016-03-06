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

#include "LaserDriverTest.h"

#include "gtest/gtest.h"

TEST(laser_driver_test, simple_test)
{
    EXPECT_EQ(1, 1);
}

TEST(laser_driver_test, convert_position_to_timing_test_empty)
{
    laser_buffer.laser_timings[0] = 100;
    laser_buffer.length = 0;
    convert_positions_to_timings();
    EXPECT_EQ(laser_buffer.laser_timings[0], 0);
}

TEST(laser_driver_test, convert_position_to_timing_test_non_empty)
{
    laser_timing_scale_dividend = 3;
    laser_timing_scale_divisor = 2;
    laser_timing_center_offset = 10000;

    laser_buffer.positions[0] = -200;
    laser_buffer.positions[1] = 200;
    laser_buffer.positions[2] = 200;
    laser_buffer.length = 3;
    convert_positions_to_timings();
    EXPECT_EQ(laser_buffer.laser_timings[0], 9700);
    EXPECT_EQ(laser_buffer.laser_timings[1], 10000);
    EXPECT_EQ(laser_buffer.laser_timings[2], 10300);
}