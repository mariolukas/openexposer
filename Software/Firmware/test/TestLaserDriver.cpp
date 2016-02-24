#include <OpenExposer/LaserDriver.h>
#include "gtest/gtest.h"
#include "TestLaserDriver.h"

TEST(laser_driver_test, simple_test)
{
    EXPECT_EQ(1, 1);
}

TEST(laser_driver_test, convert_position_to_timing_test_empty)
{
    data.laser_timings[0] = 100;
    laser_data_position = 0;
    convert_positions_to_timings();
    EXPECT_EQ(data.laser_timings[0], 0);
}

TEST(laser_driver_test, convert_position_to_timing_test_non_empty)
{
    data.positions[0] = 100;
    data.positions[1] = 200;
    data.positions[2] = 300;
    laser_data_position = 3;
    convert_positions_to_timings();
    EXPECT_EQ(data.laser_timings[0], 1500);
    EXPECT_EQ(data.laser_timings[1], 3000);
    EXPECT_EQ(data.laser_timings[2], 4500);
}