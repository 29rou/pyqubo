target_include_directories(cpp_pyqubo
  PUBLIC ${PROJECT_SOURCE_DIR}/include
  )

set_target_properties(cpp_pyqubo PROPERTIES
    CXX_VISIBILITY_PRESET "hidden"
    INTERPROCEDURAL_OPTIMIZATION TRUE
    PREFIX "${PYTHON_MODULE_PREFIX}"
    SUFFIX "${PYTHON_MODULE_EXTENSION}"
)

add_library(cpp_pyqubo_body STATIC
express.cpp
coeff.cpp
encoder.cpp
placeholderpoly.cpp
expanded.cpp
poly.cpp
)
