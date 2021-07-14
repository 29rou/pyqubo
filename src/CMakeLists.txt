target_include_directories(cpp_pyqubo
  PUBLIC ${PROJECT_SOURCE_DIR}/include
  )

set_target_properties(cpp_pyqubo PROPERTIES
    CXX_VISIBILITY_PRESET "hidden"
    INTERPROCEDURAL_OPTIMIZATION TRUE
    PREFIX "${PYTHON_MODULE_PREFIX}"
    SUFFIX "${PYTHON_MODULE_EXTENSION}"    
)

if (PYQUBO_BUILD_SHARED_LIBS)
  add_library(cpp_pyqubo_body SHARED
    ${PROJECT_SOURCE_DIR}/src/express.cpp
    ${PROJECT_SOURCE_DIR}/src/coeff.cpp
    ${PROJECT_SOURCE_DIR}/src/encoder.cpp
    ${PROJECT_SOURCE_DIR}/src/placeholderpoly.cpp
    ${PROJECT_SOURCE_DIR}/src/expanded.cpp
    ${PROJECT_SOURCE_DIR}/src/poly.cpp
  )
else()
  add_library(cpp_pyqubo_body STATIC
    ${PROJECT_SOURCE_DIR}/src/express.cpp
    ${PROJECT_SOURCE_DIR}/src/coeff.cpp
    ${PROJECT_SOURCE_DIR}/src/encoder.cpp
    ${PROJECT_SOURCE_DIR}/src/placeholderpoly.cpp
    ${PROJECT_SOURCE_DIR}/src/expanded.cpp
    ${PROJECT_SOURCE_DIR}/src/poly.cpp
  )
endif()
