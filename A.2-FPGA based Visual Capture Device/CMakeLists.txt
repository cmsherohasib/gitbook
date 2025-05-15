cmake_minimum_required(VERSION 3.17.0)
set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE INTERNAL "" FORCE)

project(SecubloxCam VERSION 0.1.1)


macro(ADD_SOURCE_FILES_FOR_MODULE MODULE_NAME)
    list(APPEND SOURCE_FILES_INCLUDE_LIST ${MODULE_NAME})
endmacro(ADD_SOURCE_FILES_FOR_MODULE)

macro(ADD_SOURCE_FILES_FOR_MODULES)
    foreach (MODULE ${ARGN})
        ADD_SOURCE_FILES_FOR_MODULE(${MODULE})
    endforeach (MODULE)
endmacro(ADD_SOURCE_FILES_FOR_MODULES)

macro(ADD_FILES_TO_MODULE_FILES_LISTS FOLDER_WITH_FILES)
    file(GLOB CURRENT_SOURCE_FILES_H ${CMAKE_CURRENT_SOURCE_DIR}/${FOLDER_WITH_FILES}/*.h )
    file(GLOB CURRENT_SOURCE_FILES_CPP ${CMAKE_CURRENT_SOURCE_DIR}/${FOLDER_WITH_FILES}/*.cpp )
    list(APPEND SOURCE_FILES_H ${CURRENT_SOURCE_FILES_H})
    list(APPEND SOURCE_FILES_CPP ${CURRENT_SOURCE_FILES_CPP})
endmacro(ADD_FILES_TO_MODULE_FILES_LISTS)

macro(CREATE_MODULE_FILES_LISTS)
    file(GLOB SOURCE_FILES_H ${CMAKE_CURRENT_SOURCE_DIR}/source/*.h ${CMAKE_CURRENT_SOURCE_DIR}/include/*.h)
    file(GLOB SOURCE_FILES_CPP ${CMAKE_CURRENT_SOURCE_DIR}/source/*.cpp ${CMAKE_CURRENT_SOURCE_DIR}/include/*.cpp)
endmacro(CREATE_MODULE_FILES_LISTS)

include(CheckCXXCompilerFlag)
check_cxx_compiler_flag("-std=c++1z" HAS_STDCXX_1z)
if (HAS_STDCXX_1z)
    ADD_COMPILE_OPTIONS("-std=c++1z")
else ()
    check_cxx_compiler_flag("/std:c++1z" HAS_STDCXX_1z_MSVC)
    if (HAS_STDCXX_1z_MSVC)
        ADD_COMPILE_OPTIONS("/std:c++1z")
    else ()
        MESSAGE("The compiler doesn't support the 1z C++ standard")
        exit()
    endif ()
endif ()

link_directories(${CMAKE_SOURCE_DIR}/SecubloxNetCam/lib)

set(JSON_BuildTests OFF CACHE INTERNAL "")    # skip json test suite
add_subdirectory(contrib/nlohmann/json)

add_subdirectory(src/jpeg)
add_subdirectory(src/stream_encryption)

add_subdirectory(SecubloxViewerDemo)
