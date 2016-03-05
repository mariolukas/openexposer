#Open Exposer Firmware

The firmware for the Open Exposer supports right now only the Arduino UNO. The goal is to make the firmware work on different microcontrollers.

## Build

The simplest way to build the firmware is by opening the OpenExposer.ino-Sketch in the OpenExposer directory with the Arduino-IDE `>= 1.6.6`. This builds just the binary to be flashed to the microcontroller. 

Additionally cmake can be used to build the firmware hex-file and compile and run unit tests. It works with cmake version `2.8.12`.

To build the firmware go into the `Firmware` directory and create a new directory `build` and make it the current directory

    $ mkdir build
    $ cd build

Then create the make files:

    $ cmake ..
    -- The C compiler identification is GNU 4.8.4
    -- The CXX compiler identification is GNU 4.8.4
    -- Check for working C compiler: /usr/bin/cc
    -- Check for working C compiler: /usr/bin/cc -- works
    -- Detecting C compiler ABI info
    -- Detecting C compiler ABI info - done
    -- Check for working CXX compiler: /usr/bin/c++
    -- Check for working CXX compiler: /usr/bin/c++ -- works
    -- Detecting CXX compiler ABI info
    -- Detecting CXX compiler ABI info - done
    -- Found Git: /usr/bin/git (found version "1.9.1") 
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /home/christoph/Documents/Projects/openexposer/Software/Firmware/build

Now you can create the firmware with the command:

    $ make OpenExposerFirmware
    [ 12%] Creating directories for 'OpenExposerFirmware'
    [ 25%] No download step for 'OpenExposerFirmware'
    [ 37%] No patch step for 'OpenExposerFirmware'
    [ 50%] No update step for 'OpenExposerFirmware'
    [ 62%] Performing configure step for 'OpenExposerFirmware'
    -- Generating OpenExposerFirmware
    -- Generating uno_OpenExposer for library OpenExposer
    -- Using /home/christoph/arduino-1.6.7/hardware/tools/avr/bin/avr-objcopy for converting firmware image to hex
    -- Configuring done
    -- Generating done
    -- Build files have been written to: /home/christoph/Documents/Projects/openexposer/Software/Firmware/build/OpenExposerFirmware/src/OpenExposerFirmware-build
    [ 75%] Performing build step for 'OpenExposerFirmware'
    [ 80%] Built target uno_CORE
    [ 93%] Built target uno_OpenExposer
    Scanning dependencies of target OpenExposerFirmware
    [ 96%] Building CXX object CMakeFiles/OpenExposerFirmware.dir/OpenExposerFirmware_OpenExposer.ino.cpp.obj
    Linking CXX executable /home/christoph/Documents/Projects/openexposer/Software/Firmware/build/OpenExposerFirmware.elf
    Generating EEP image
    Generating HEX image
    Calculating image size
    Firmware Size:  [Program: 13470 bytes (41.1%)]  [Data: 1479 bytes (72.2%)] on atmega328p
    EEPROM   Size:  [Program: 0 bytes (0.0%)]  [Data: 0 bytes (0.0%)] on atmega328p
    
    [100%] Built target OpenExposerFirmware
    [ 87%] Performing install step for 'OpenExposerFirmware'
    [ 80%] Built target uno_CORE
    [ 93%] Built target uno_OpenExposer
    [100%] Built target OpenExposerFirmware
    Install the project...
    -- Install configuration: ""
    Not installing the firmware.
    [100%] Completed 'OpenExposerFirmware'
    [100%] Built target OpenExposerFirmware

The hex-file named `ÒpenExposerFirmware.hex` can be found in the build directory.

In order to run the tests, you call make with the arguments:

    $ make OpenExposerTests && make test
    [  6%] Creating directories for 'googletest'
   
    ...
    
    [100%] Built target OpenExposerTests
    Running tests...
    Test project /home/christoph/Documents/Projects/openexposer/Software/Firmware/build
        Start 1: OpenExposerTests
    1/1 Test #1: OpenExposerTests .................   Passed    0.00 sec
    
    100% tests passed, 0 tests failed out of 1
    
    Total Test time (real) =   0.01 sec

## Troubleshooting
If make can't find your arduino sdk, it complains with an error message:

    [ 21%] Performing configure step for 'OpenExposerFirmware'
    CMake Error at /home/christoph/Documents/Projects/openexposer/Software/Firmware/cmake/ArduinoToolchain.cmake:83 (message):
      Could not find Arduino SDK (set ARDUINO_SDK_PATH)!

You can solve this issue by exporting an environment variable `ARDUINO_SDK_PATH`which contains the path of the arduino sdk.

    $ export ARDUINO_SDK_PATH=<here the path to arduino>
    


