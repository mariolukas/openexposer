cmake_minimum_required(VERSION 2.8.8)
set(PROJECT_NAME OpenExposer)
project(${PROJECT_NAME})


if(CMAKE_COMPILER_IS_GNUCXX)
    add_definitions(-Wall -Wno-deprecated)
endif()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -Wextra -pthread")

include_directories(
        ${PROJECT_SOURCE_DIR}
)
#-------------------
# set common include folder for module
#-------------------
set(TEST_INCLUDES ${PROJECT_SOURCE_DIR}/test-include)
set(EXT_PROJECTS_DIR ${PROJECT_SOURCE_DIR}/ext)
set(PROJECT_TEST_DIR ${PROJECT_SOURCE_DIR}/test)

#-------------------
# Module source
#-------------------
set(PROJECT_LIB_NAME ${PROJECT_NAME_STR}_impl)

#include_directories(${COMMON_INCLUDES})
file(GLOB SRC_FILES ${PROJECT_SOURCE_DIR}/OpenExposer/*.cpp)
add_library(${PROJECT_LIB_NAME} ${SRC_FILES})

add_subdirectory(${EXT_PROJECTS_DIR}/gtest)

#-------------------
# Test
#-------------------
enable_testing()
set(PROJECT_TEST_NAME ${PROJECT_NAME}_test)
include_directories(${GTEST_INCLUDE_DIRS} ${TEST_INCLUDES} ${PROJECT_TEST_DIR})
set(TEST_SRC_FILES test/TestLaserDriver.cpp test/FakeSerial.cpp test/ArduinoSymbols.cpp)
add_executable(${PROJECT_TEST_NAME} ${TEST_SRC_FILES})
add_dependencies(${PROJECT_TEST_NAME} googletest)


if(NOT WIN32)
    target_link_libraries(${PROJECT_TEST_NAME}
            ${PROJECT_LIB_NAME}
            ${GTEST_LIBS_DIR}/libgtest.a
            ${GTEST_LIBS_DIR}/libgtest_main.a
            )
else()
    target_link_libraries(${PROJECT_TEST_NAME}
            debug ${GTEST_LIBS_DIR}/DebugLibs/${CMAKE_FIND_LIBRARY_PREFIXES}gtest${CMAKE_FIND_LIBRARY_SUFFIXES}
            optimized ${GTEST_LIBS_DIR}/ReleaseLibs/${CMAKE_FIND_LIBRARY_PREFIXES}gtest${CMAKE_FIND_LIBRARY_SUFFIXES}
            )
    target_link_libraries(${PROJECT_TEST_NAME}
            debug ${GTEST_LIBS_DIR}/DebugLibs/${CMAKE_FIND_LIBRARY_PREFIXES}gtest_main${CMAKE_FIND_LIBRARY_SUFFIXES}
            optimized ${GTEST_LIBS_DIR}/ReleaseLibs/${CMAKE_FIND_LIBRARY_PREFIXES}gtest_main${CMAKE_FIND_LIBRARY_SUFFIXES}
            )
endif()

target_link_libraries(${PROJECT_TEST_NAME} ${CMAKE_THREAD_LIBS_INIT})

add_test(test1 ${PROJECT_TEST_NAME})

set(OpenExposer_PREFIX ${CMAKE_BINARY_DIR}/OpenExposer_Firmware)

include(ExternalProject)

ExternalProject_Add(OpenExposer_Firmware
        SOURCE_DIR ${OpenExposer_SOURCE_DIR}/OpenExposer
        )
