#!/usr/bin/python
#
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

import os, sys, platform, getopt, subprocess

def print_help():
    print ''
    print 'build.py valid options...'
    print ''
    print 'release: build for release, default is debug'
    print '    arm: cross compilation for arm on x86/64 host'
    print '         you need to create ARM Rootfs and'
    print '         set ROOTFS_ARM environment to that folder'
    print '  clean: clean output before building'
    print '      p: parallel build (-j4)'
    print ''
    return

def get_cmake_defines(define, value):
    return '-D' + define + '=' + value + ' '

def get_cmake_cross(str_system):
    cfg_system_cmake = 'config_' + str_system + '.cmake'
    return get_cmake_defines('CMAKE_TOOLCHAIN_FILE', './cmake/config/' + cfg_system_cmake)

# system name, architecture
this_platform = sys.platform
if this_platform == 'linux2':
    this_platform = 'linux'
this_process = platform.processor()

# configuration setting initial values
this_system =  this_process + "-" + this_platform
this_type = 'debug'
this_cross = False
do_clean = False
do_parallel = False

# set settings from parameters
for arg in sys.argv :
    if arg == 'release':
        this_type = arg
    elif arg == 'clean':
        do_clean = True
    elif arg == 'arm':
        this_system = 'armv7l-linux'
        this_cross = True
    elif arg == 'p':
        do_parallel = True
    elif arg == 'help':
        print_help()
        sys.exit()

#
# set cmake parameters
#

# output folder
out_folder = 'bin'
# build path
build_path = os.path.join("./", out_folder)
build_path = os.path.join(build_path, this_system)
build_path = os.path.join(build_path, this_type)
# cmake folder in build path
cmake_path = os.path.join(build_path, 'cmake')
# base and home
cmake_base = '-B' + cmake_path
cmake_home = '-H./'
# cmake defines
cmake_defines  = get_cmake_defines('CMAKE_BUILD_TYPE', this_type)
cmake_defines += get_cmake_defines('TARGET_PLATFORM', this_system)
if this_cross:
    cmake_defines += get_cmake_cross(this_system)

# parallel
cmake_parallel = ""
if do_parallel:
    cmake_parallel = " -- -j4"

# for debugging
# print 'cmake_path = ' + cmake_path
# print 'cmake ' + cmake_base + ' ' + cmake_home + ' ' + cmake_defines

# show default help message
print ''
print '"./build.py help" to see options.'
print ''

# do post build
if do_clean:
    os.system('rm -rf ./' + out_folder + '/*')
    print 'Cleaning done.'

# run cmake and make
os.system('mkdir -p ' + cmake_path)
os.system('cmake ' + cmake_base + ' ' + cmake_home + ' ' + cmake_defines)
os.system('cmake --build ' + cmake_path + cmake_parallel)
