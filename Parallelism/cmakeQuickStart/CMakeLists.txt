cmake_minimum_required(VERSION 3.0.0)
project(sinus_sum VERSION 0.1.0 LANGUAGES C CXX)

option(USE_FLOAT "Use float type for array elements" OFF)

add_executable(sinus_sum main.cpp)

if(USE_DOUBLE)
    target_compile_definitions(sinus_sum PRIVATE USE_DOUBLE)
endif()