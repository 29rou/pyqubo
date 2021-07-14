cmake_minimum_required(VERSION 3.11)

project(cpp_pyqubo)

set(CMAKE_INTERPROCEDURAL_OPTIMIZATION True)

set(CXX_STANDARD_REQUIRED TRUE)
set(CMAKE_VERBOSE_MAKEFILE TRUE)

set(CMAKE_CXX_STANDARD 14)
# Set default compile flags for GCC
if(CMAKE_COMPILER_IS_GNUCXX)
    message(STATUS "GCC detected, adding compile flags")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wno-long-long -pedantic")
else(CMAKE_COMPILER_IS_GNUCXX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
endif(CMAKE_COMPILER_IS_GNUCXX)


# add fPIC option to all object files
set(CMAKE_POSITION_INDEPENDENT_CODE ON)


##### Set default behavior #####
set(DEFAULT_USE_OMP Yes)

# Use OpenMP as default behavior
if(NOT DEFINED USE_OMP)
    set(USE_OMP ${DEFAULT_USE_OMP})
endif()

message(STATUS "USE_OMP = ${USE_OMP}")


if(USE_OMP)
    find_package(OpenMP REQUIRED)
    if(OpenMP_FOUND)
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
        add_definitions(-DUSE_OMP)
    endif()
endif()

if (APPLE)
    find_package(BLAS)
endif()
list(APPEND CMAKE_MODULE_PATH external)
include(${CMAKE_SOURCE_DIR}/external/pybind11.cmake)
#include(${CMAKE_SOURCE_DIR}/external/cimod.cmake)
include_directories(cpp_dimod)

add_subdirectory(pybind11)
pybind11_add_module(cpp_pyqubo src/pybind_mapping.cpp)

# VERSION_INFO is defined by setup.py and passed into the C++ code as a define (VERSION_INFO) here.
target_compile_definitions(cpp_pyqubo PRIVATE VERSION_INFO=${PYQUBO_VERSION_INFO})

add_subdirectory(src)


include(${CMAKE_SOURCE_DIR}/external/googletest.cmake)
add_subdirectory(tests)
