cmake_minimum_required(VERSION 3.18)
project(pypoints2grid)

set(CMAKE_CXX_STANDARD 11)
set(BINDINGS _points2grid)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

find_package(Python 3.10 COMPONENTS Interpreter Development.Module REQUIRED)

execute_process(
    COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE pybind11_DIR)

message(STATUS "Set pybind11_DIR to ${pybind11_DIR}")
find_package(pybind11 REQUIRED CONFIG)

include_directories(${CMAKE_SOURCE_DIR}/src/include)
include_directories(${CMAKE_SOURCE_DIR}/src/contrib)

pybind11_add_module(${BINDINGS} ${CMAKE_SOURCE_DIR}/src/pybind_points2grid.cpp)
install(TARGETS ${BINDINGS} DESTINATION pypoints2grid)
