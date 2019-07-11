# Searches for CppAD includes and library files
#
# Sets the variables
#   CppAD_FOUND
#   CppAD_INCLUDE_DIR
#   CppAD_LIBRARIES

SET (CppAD_FOUND FALSE)

FIND_PATH (CppAD_INCLUDE_DIR cppad.hpp
    /usr/include/cppad
    /usr/local/include/cppad
    $ENV{HOME}/local/include/cppad
    ${CMAKE_INSTALL_PREFIX}/include/cppad
    $ENV{CppAD_PATH}/src/cppad
    $ENV{CppAD_PATH}/include/cppad
    $ENV{CppAD_INCLUDE_PATH}
)

FIND_LIBRARY (CppAD_LIBRARY NAMES cppad_lib	PATHS
    /usr/lib
    /usr/local/lib
    ${CMAKE_INSTALL_PREFIX}/lib
    $ENV{HOME}/local/lib
    $ENV{CppAD_LIBRARY_PATH}
)

IF (CppAD_INCLUDE_DIR AND CppAD_LIBRARY)
    SET (CppAD_FOUND TRUE)
ENDIF (CppAD_INCLUDE_DIR AND CppAD_LIBRARY)

IF (CppAD_FOUND)
   IF (NOT CppAD_FIND_QUIETLY)
      MESSAGE(STATUS "Found CppAD: ${CppAD_LIBRARY}")
   ENDIF (NOT CppAD_FIND_QUIETLY)
ELSE (CppAD_FOUND)
   IF (CppAD_FIND_REQUIRED)
      MESSAGE(FATAL_ERROR "Could not find CppAD")
   ENDIF (CppAD_FIND_REQUIRED)
ENDIF (CppAD_FOUND)

MARK_AS_ADVANCED (
    CppAD_FOUND
    CppAD_INCLUDE_DIR
    CppAD_LIBRARIES
)

