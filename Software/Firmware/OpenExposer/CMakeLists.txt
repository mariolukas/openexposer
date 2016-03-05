cmake_minimum_required(VERSION 2.8.8)

set(CMAKE_TOOLCHAIN_FILE ${CMAKE_SOURCE_DIR}/../cmake/ArduinoToolchain.cmake)
set(PROJECT_NAME OpenExposerFirmware)

project(${PROJECT_NAME})

set(${CMAKE_PROJECT_NAME}_SKETCH OpenExposer.ino)

option(BINARY_DIRECTORY "Directory for the binaries" ${CMAKE_BINARY_DIR})
set(EXECUTABLE_OUTPUT_PATH ${BINARY_DIRECTORY})


if(CMAKE_COMPILER_IS_GNUCXX)
    add_definitions(-Wall -Wno-deprecated -std=c++11)
endif()

generate_arduino_firmware(${CMAKE_PROJECT_NAME})

install(CODE "MESSAGE(\"Not installing the firmware.\")")
#install(TARGETS ${CMAKE_PROJECT_NAME} RUNTIME DESTINATION .)