# Copyright 2018 saehie.park@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cmake_minimum_required(VERSION 2.8.12)

project(tflite)

include(cmake/options.cmake)

#
# Tensorflow Lite library
#
set(TFL_LIBNAME "tensorflow-lite")

file(GLOB TFLITE_SRCS 
      "*.cc"
      "kernels/*.cc"
      "kernels/internal/*.cc"
      "kernels/internal/optimized/*.cc"
      "kernels/internal/reference/*.cc"
      "*.c"
      "kernels/*.c"
      "kernels/internal/*.c"
      "kernels/internal/optimized/*.c"
      "kernels/internal/reference/*.c"
      "downloads/farmhash/src/farmhash.cc"
      )

foreach(item ${TFLITE_SRCS})
  if("${item}" MATCHES "_test.cc" OR "${item}" MATCHES "test_util.cc")
    list(REMOVE_ITEM TFLITE_SRCS ${item})
  endif()
endforeach()
# message(STATUS "${TFLITE_SRCS}")

# user lib libsomething for arm
# set(LIBUSER $ENV{HOME}/bin/libsomething.arm)
set(PROJ_INCLUDES ${PROJ_INCLUDES} 
    "${CMAKE_CURRENT_SOURCE_DIR}/../../../"
    "${CMAKE_CURRENT_SOURCE_DIR}/downloads/"
    "${CMAKE_CURRENT_SOURCE_DIR}/downloads/eigen"
    "${CMAKE_CURRENT_SOURCE_DIR}/downloads/gemmlowp"
    "${CMAKE_CURRENT_SOURCE_DIR}/downloads/neon_2_sse"
    "${CMAKE_CURRENT_SOURCE_DIR}/downloads/farmhash/src"
    "${CMAKE_CURRENT_SOURCE_DIR}/downloads/flatbuffers/include"
    )
# set(PROJ_USER_LIBDIR ${LIBUSER}/lib)
# set(PROJ_USER_LIBNAME "something")
set(TFLITE_LIBSFOREXE
    "stdc++" 
    "pthread"
    "m"
    "z"
    "dl"
    )

add_library(${TFL_LIBNAME} ${TFLITE_SRCS})
target_include_directories(${TFL_LIBNAME} SYSTEM PRIVATE ${TARGET_INC})
target_include_directories(${TFL_LIBNAME} PUBLIC ${PROJ_INCLUDES})
set_target_properties(${HELLOWORLD} PROPERTIES
                      ARCHIVE_OUTPUT_DIRECTORY "${PROJ_LIB_OUT}"
                      LIBRARY_OUTPUT_DIRECTORY "${PROJ_LIB_OUT}"
                      RUNTIME_OUTPUT_DIRECTORY "${PROJ_BIN_OUT}"
                      )

#
# example label_image
#
set(LABEL_IMAGE "label_image")

set(LABEL_IMAGE_SRCS
    "${CMAKE_CURRENT_SOURCE_DIR}/examples/label_image/bitmap_helpers.cc"
    "${CMAKE_CURRENT_SOURCE_DIR}/examples/label_image/label_image.cc"
    )
set(LABEL_IMAGE_INCS
    "${CMAKE_CURRENT_SOURCE_DIR}/examples/label_image"
    )

# link_directories(${CMAKE_SOURCE_DIR}/libarm)

add_executable(${LABEL_IMAGE} ${LABEL_IMAGE_SRCS})
target_include_directories(${LABEL_IMAGE} SYSTEM PRIVATE ${TARGET_INC})
target_include_directories(${LABEL_IMAGE} PUBLIC ${PROJ_INCLUDES} ${LABEL_IMAGE_INCS})
target_link_libraries(${LABEL_IMAGE} LINK_PUBLIC ${PROJ_LIBS} ${TFL_LIBNAME} ${TFLITE_LIBSFOREXE})
set_target_properties(${LABEL_IMAGE} PROPERTIES
                        ARCHIVE_OUTPUT_DIRECTORY "${PROJ_LIB_OUT}"
                        LIBRARY_OUTPUT_DIRECTORY "${PROJ_LIB_OUT}"
                        RUNTIME_OUTPUT_DIRECTORY "${PROJ_BIN_OUT}"
                        )

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/downloads/quantized_models/mobilenet_quant_v1_224.tflite"
               "${PROJ_BIN_OUT}/mobilenet_quant_v1_224.tflite"
               COPYONLY
               )
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/downloads/quantized_models/labels.txt"
               "${PROJ_BIN_OUT}/labels.txt"
               COPYONLY
               )
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/examples/label_image/testdata/grace_hopper.bmp"
               "${PROJ_BIN_OUT}/grace_hopper.bmp"
               COPYONLY
               )
