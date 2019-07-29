set(MASTER_PROJECT_NAME ${PROJECT_NAME})
project(${MASTER_PROJECT_NAME}_develop)

# Libraries linker
get_target_property(DEBUG_POSTFIX ${MASTER_PROJECT_NAME} DEBUG_POSTFIX)
IF(CMAKE_BUILD_TYPE MATCHES "Debug")
    SET(${MASTER_PROJECT_NAME}_LIB_NAME ${MASTER_PROJECT_NAME}${DEBUG_POSTFIX})
else()
    SET(${MASTER_PROJECT_NAME}_LIB_NAME ${MASTER_PROJECT_NAME})
endif()
if (APPLE)
    string(CONCAT ${MASTER_PROJECT_NAME}_LIB_NAME "lib" ${${MASTER_PROJECT_NAME}_LIB_NAME} ".dylib")
elseif (UNIX)
    string(CONCAT ${MASTER_PROJECT_NAME}_LIB_NAME "lib" ${${MASTER_PROJECT_NAME}_LIB_NAME} ".so")
elseif(_WIN32)
    message("TO BE TESTED")
    string(CONCAT ${MASTER_PROJECT_NAME}_LIB_NAME ${${MASTER_PROJECT_NAME}_LIB_NAME} ".dll")
endif()
set(${MASTER_PROJECT_NAME}_LIBRARY ${CMAKE_BINARY_DIR}/${${MASTER_PROJECT_NAME}_LIB_NAME})

# Copy the c3d of the example
file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/pyomecaman.bioMod
     DESTINATION ${CMAKE_CURRENT_BINARY_DIR})


# CPP_AD Development project
find_package(CppAD REQUIRED)

add_executable(cppAD_dev "cppAD.cpp")
target_include_directories(cppAD_dev PUBLIC
    ${RBDL_INCLUDE_DIR}
    ${RBDL_INCLUDE_DIR}/..
    ${Boost_INCLUDE_DIRS}
    ${EIGEN3_INCLUDE_DIR}
    ${DLIB_INCLUDE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../include
    ${CppAD_INCLUDE_DIR}
)
target_link_libraries(cppAD_dev ${${MASTER_PROJECT_NAME}_LIBRARY} ${RBDL_LIBRARY} ${CppAD_LIBRARIES})

