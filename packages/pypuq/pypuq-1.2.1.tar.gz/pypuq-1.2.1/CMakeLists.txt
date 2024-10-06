cmake_minimum_required(VERSION 3.22)
cmake_policy(SET CMP0074 NEW)
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

project(PUQ VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -Wno-deprecated -O3")
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# compile libraries and executables
###################################

message("Code version: ${CODE_VERSION}")

find_package(SCNT-EXS REQUIRED)

message("Building library: puq-cpp")
file(GLOB source_files "src/*.cpp" "src/**/*.cpp")
add_library(puq-cpp STATIC ${source_files})
target_compile_definitions(puq-cpp PRIVATE CONFIG_FILE="../src/config.h")

message("Compiling executable: puq")
file(GLOB example_files "exec/puq/*.cpp" "exec/puq/**/*.cpp")
add_executable(puq ${example_files} )
target_compile_definitions(puq PRIVATE CODE_VERSION="${CODE_VERSION}")
target_link_libraries(puq PRIVATE puq-cpp)

message("Compiling executable: dmap")
file(GLOB example_files "exec/dmap/*.cpp" "exec/dmap/**/*.cpp")
add_executable(dmap ${example_files} )
target_compile_definitions(dmap PRIVATE CODE_VERSION="${CODE_VERSION}")
target_link_libraries(dmap PRIVATE puq-cpp)

install(TARGETS puq DESTINATION bin)

# add Google tests
###################

find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})
enable_testing()

file(GLOB test_files "gtest/*.cpp")
add_executable(TestSolver ${test_files})
target_link_libraries(TestSolver PRIVATE GTest::gtest_main puq-cpp)

include(GoogleTest)
gtest_discover_tests(TestSolver)

# add Google benchmark
######################

find_package(benchmark REQUIRED)

file(GLOB test_files "benchmark/*.cpp")
add_executable(Benchmark ${test_files})
target_link_libraries(Benchmark PRIVATE benchmark::benchmark puq-cpp)

# create pydipl module for Python
#################################

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
include_directories(${Python3_INCLUDE_DIRS})
find_package(pybind11 CONFIG)

pybind11_add_module(pypuq exec/pypuq/pypuq.cpp)
target_link_libraries(pypuq PRIVATE puq-cpp)
target_compile_definitions(pypuq PRIVATE CODE_VERSION="${CODE_VERSION}")
