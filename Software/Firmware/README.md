#Open Exposer Firmware

The firmware for the Open Exposer supports right now only the Arduino UNO. The goal is to make the firmware work on different microcontrollers.

## Build

The simplest way to build the firmware is by opening the OpenExposer.ino-Sketch in the OpenExposer directory with the Arduino-IDE and hitting build. This builds jsut the binary to be flashed to the microcontroller.

Additionally cmake can be used to build the firmware hex-file and compile and run unit tests.
Therefore you need to install cmake.
