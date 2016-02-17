cmake_minimum_required(VERSION 2.8.8)
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_SOURCE_DIR}/../cmake/ArduinoToolchain.cmake)
set(PROJECT_NAME OpenExposer)
project(${PROJECT_NAME})

set(${CMAKE_PROJECT_NAME}_SKETCH OpenExposer.ino)
generate_arduino_firmware(${CMAKE_PROJECT_NAME})


if(CMAKE_COMPILER_IS_GNUCXX)
    add_definitions(-Wall -Wno-deprecated)
endif()
