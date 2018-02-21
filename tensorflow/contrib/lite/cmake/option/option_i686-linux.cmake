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

#
# config for i686-linux
#
include(CMakeForceCompiler)

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR i686)

# set linux common flags
include("cmake/option/option_linux-common.cmake")

# SIMD for x86: My ATOM doesn't support sse4 so disable SIMD
set(FLAGS_COMMON ${FLAGS_COMMON}
    "-DGEMMLOWP_ALLOW_SLOW_SCALAR_FALLBACK"
    )

# no additional target includes
set(TARGET_INC )
