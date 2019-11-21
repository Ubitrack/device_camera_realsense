# All cpp files for realsense2 camera capture
set(UBITRACK_LIBRARY_NAME "realsense2camera")

FILE(GLOB UBITRACK_SRCS RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
   "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp"
)

FILE(GLOB UBITRACK_HDRS RELATIVE "${CMAKE_CURRENT_SOURCE_DIR}"
        "${CMAKE_CURRENT_SOURCE_DIR}/*.h"
        )

add_library(${UBITRACK_LIBRARY_NAME} SHARED ${UBITRACK_SRCS} ${UBITRACK_HDRS})


# Special case librealsense-file is a static library which contains symbols that are not exported if not referenced
# for ubitrack we use dynamic libraries, and we need to force the linker to include all symbols
# there is no proper way to do this in CMake and it is not platform independent
# currently only a solution for gcc is implemented.
find_library(LIBREALSENSE_FILE_LIBRARY ${LIBREALSENSE_FILE_LIBNAME})

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  # using Clang
  MESSAGE(STATUS "WARNING: Librealsense-File is probably not linked correctly")
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
  # using GCC
  set(LIBREALSENSE_FILE_LIBRARY "-Wl,--whole-archive ${LIBREALSENSE_FILE_LIBRARY} -Wl,--no-whole-archive")
  MESSAGE(STATUS "Realsense-File Linking: ${LIBREALSENSE_FILE_LIBRARY}")
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Intel")
  # using Intel C++
  MESSAGE(STATUS "WARNING: Librealsense-File is probably not linked correctly")
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
  # using Visual Studio C++
  # Check /WHOLEARCHIVE Linker Flag
  MESSAGE(STATUS "WARNING: Librealsense-File is probably not linked correctly")
endif()



target_link_libraries(${UBITRACK_LIBRARY_NAME} PUBLIC
    CONAN_PKG::ubitrack_core
    CONAN_PKG::ubitrack_vision
    CONAN_PKG::ubitrack_dataflow
    CONAN_PKG::ubitrack_dataflow
    CONAN_PKG::librealsense
    ${LIBREALSENSE_FILE_LIBRARY}
    OpenGL::GL
    OpenGL::GLU
    ${UBITRACK_EXTRA_LIBS}
    )

if(WITH_OPENCL)
  target_link_libraries(${UBITRACK_LIBRARY_NAME} PUBLIC
      OpenCL::OpenCL
  )
endif()

target_include_directories(${UBITRACK_LIBRARY_NAME} PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<BUILD_INTERFACE:${CONAN_INCLUDE_DIRS_LIBREALSENSE}>
        PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# do not create symlinks to versioned names of component libraries
set_target_properties(${UBITRACK_LIBRARY_NAME} PROPERTIES NO_SONAME ON)

# Apply Target Properties
if(MSVC)
  if(CMAKE_CROSSCOMPILING)
    set_target_properties(${UBITRACK_LIBRARY_NAME} PROPERTIES LINK_FLAGS "/NODEFAULTLIB:secchk")
  endif()
  set_target_properties(${UBITRACK_LIBRARY_NAME} PROPERTIES LINK_FLAGS "/NODEFAULTLIB:libc /DEBUG")
endif()

ubitrack_set_target_properties(${UBITRACK_LIBRARY_NAME})
ubitrack_install_component(${UBITRACK_LIBRARY_NAME})
