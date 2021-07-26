include(FetchContent)

#### pybind11 ####
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY  https://github.com/pybind/pybind11
    GIT_TAG         v2.6.2
)
ser(EIGEN_MPL2_ONLY ON)
set(EIGEN_CPP_STANDARD -std=c++11)
FetchContent_MakeAvailable(pybind11)
