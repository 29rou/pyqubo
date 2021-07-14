cmake_minimum_required(VERSION 3.18)

project(cpp_pyqubo CXX)

set(CMAKE_INTERPROCEDURAL_OPTIMIZATION True)

set(CXX_STANDARD_REQUIRED TRUE)
set(CMAKE_VERBOSE_MAKEFILE TRUE)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_CXX_STANDARD 14)

option(PYQUBO_BUILD_SHARED_LIBS "build mylib as a shared library" ON)


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
        target_compile_options(cpp_pyqubo PUBLIC ${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS})
        add_definitions(-DUSE_OMP)
    endif()
endif()

if (APPLE)
    find_package(BLAS)
endif()


list(APPEND CMAKE_MODULE_PATH external)

include(FetchContent)


if(USE_TEST)
       include(${PROJECT_SOURCE_DIR}/external/googletest.cmake)     
       FetchContent_MakeAvailable(googletest)
       add_subdirectory(tests)
else()
	message(STATUS "Skip downloding googletest")
endif()

include(${PROJECT_SOURCE_DIR}/external/pybind11.cmake)
FetchContent_MakeAvailable(pybind11)
#include(${CMAKE_SOURCE_DIR}/external/cimod.cmake)
include_directories(cpp_dimod)

find_package(pybind11 CONFIG REQUIRED)

add_subdirectory(src)

if (PYQUBO_BUILD_SHARED_LIBS)
  pybind11_add_module(cpp_pyqubo SHARED
    ${PROJECT_SOURCE_DIR}/pybind_mapping.cpp
    ${PROJECT_SOURCE_DIR}/express.cpp
    ${PROJECT_SOURCE_DIR}/coeff.cpp
    ${PROJECT_SOURCE_DIR}/encoder.cpp
    ${PROJECT_SOURCE_DIR}/placeholderpoly.cpp
    ${PROJECT_SOURCE_DIR}/expanded.cpp
    ${PROJECT_SOURCE_DIR}/poly.cpp
  )
else()
  pybind11_add_module(cpp_pyqubo MODULE
    ${PROJECT_SOURCE_DIR}/pybind_mapping.cpp
    ${PROJECT_SOURCE_DIR}/express.cpp
    ${PROJECT_SOURCE_DIR}/coeff.cpp
    ${PROJECT_SOURCE_DIR}/encoder.cpp
    ${PROJECT_SOURCE_DIR}/placeholderpoly.cpp
    ${PROJECT_SOURCE_DIR}/expanded.cpp
    ${PROJECT_SOURCE_DIR}/poly.cpp
  )
endif()
