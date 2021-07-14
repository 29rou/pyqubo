target_include_directories(cpp_pyqubo
  PUBLIC ${PROJECT_SOURCE_DIR}/include
  )

add_library(cpp_pyqubo_body STATIC
express.cpp
coeff.cpp
encoder.cpp
placeholderpoly.cpp
expanded.cpp
poly.cpp
)
