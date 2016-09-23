cmake_minimum_required(VERSION 3.0)
project(NeMo)
enable_testing()

INCLUDE_DIRECTORIES(${ROSS_SOURCE_DIR} ${ROSS_BINARY_DIR})
set (CMAKE_EXPORT_COMPILE_COMMANDS 1 )

##NeMo uses a few C11 features, including generic macros. We assume standard C11
##behaviors.
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=gnu11")

## Model Version
LIST(APPEND CMAKE_MODULE_PATH "${ROSS_SOURCE_DIR}/cmake/")
#INCLUDE(GetGitRevisionDescription)
#GET_GIT_HEAD_REVISION(GIT_RESPEC_MODEL GIT_SHA1_MODEL)
set(COMPILE_PYTHON FALSE CACHE BOOL "Compile Python based neuron generator?" )
if(${COMPILE_PYTHON})
#FIND_PATH(PYTHON_INCLUDE_DIR NAMES Python.h include/python3.5m PATHS /Users/markplagge/anaconda/envs/nemo/ /Users/markplagge/anaconda/envs/nemo/include/python3.5m HINTS /Users/markplagge/anaconda/envs/nemo/include/python3.5m /usr/include/python3.5 PATHS /Users/markplagge/anaconda/envs/nemo/include/ include/python3.5  DOC "Location of Python3 headers" )
#FIND_PATH(PYTHON_LIB NAMES ctypes /python3.5/ctypes/ /python3.5/lib PATHS /Users/markplagge/anaconda/envs/NeMo/lib /usr/lib DOC "Location of Python3 lib config folder")
#set(DO_PYHOME TRUE CACHE BOOL "Set python home env setting?")
#find_path(PYHOME NAMES envs python3.5 python3 PATHS ~/anaconda DOC "Python home folder")
find_file(PYBIN NAMES python3 PATHS ~/anaconda/ /usr/local/lib/python3.5/ DOC "Python3 Binary Location")
endif()

IF(${COMPILE_PYTHON})
 #   execute_process(COMMAND echo ${PYTHON_LIB})
 #   if(${DO_PYHOME})
  #      execute_process(COMMAND set PYTHONHOME=${PYHOME})
   # endif()
    #execute_process(COMMAND python3.5-config --cflags OUTPUT_VARIABLE PYTHON_COMP_FLAGS )
    #execute_process(COMMAND python3.5-config --ldflags OUTPUT_VARIABLE PYTHON_LIB)
    #set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -I${PYTHON_INCLUDE_DIR} -Wno-unused-result -Wsign-compare -Wunreachable-code -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -arch x86_64 ")
    #set(CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} -L${PYTHON_LIB} -lpython3.5m -ldl -framework CoreFoundation -Wl")
endif()

## Model Compile-Time Options (Will add more later)
set(NeMo_NEURONS_IN_CORE 256 CACHE STRING "The number of neurons in each simulated core")
set(NeMo_NUM_WEIGHTS_IN_NEURON 4 CACHE STRING "How many weights does a neuron have? (4 is TN default)")
set(NeMo_SAVE_MSG FALSE CACHE BOOL "Save message paths to CSV or Couch? (debug messages)")
set(NeMo_SAVE_MSG_COUCH FALSE CACHE BOOL "Save message paths directly to couch?")
set(NeMo_COUCH_ADD "None" CACHE STRING "The IP address:PORT of the couch database if used")


set(SAVE_MSGS 0)
set(USE_COUCH 0)
if(NeMo_SAVE_MSG)
    set(SAVE_MSGS 1)
    if(NeMo_SAVE_MSG_COUCH)
        set(USE_COUCH 1)
    endif()
endif()

## Build Configuration Header File
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_BINARY_DIR})
#generated config files:
CONFIGURE_FILE(${CMAKE_CURRENT_SOURCE_DIR}/nemo_config.h.in ${CMAKE_CURRENT_BINARY_DIR}/nemo_config.h @ONLY)
SET_SOURCE_FILES_PROPERTIES(${CMAKE_CURRENT_SOURCE_DIR}/nemo_config.h.in PROPERTIES GENERATED FALSE)
SET_SOURCE_FILES_PROPERTIES(${CMAKE_CURRENT_BINARY_DIR}/nemo_config.h PROPERTIES GENERATED TRUE)





set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")


#Source Files:
set(model_srcs
        nemo_main.c
        globals.h
        globals.c
        neuro/synapse.h
        neuro/synapse.c

        neuro/axon.h
        neuro/axon.c

        neuro/tn_neuron.c
        neuro/tn_neuron.h

        tests/nemo_tests.h
        tests/synapse_test.c
        tests/bio_validation.c
        tests/mapping_tests.c



        mapping.c
        mapping.h


        IO/IOStack.c
        IO/IOStack.h

        IO/output.h
        IO/output.c
        nemo_config.h 
        nemo_main.h )
set(gen_srcs
        scripts/tn_neuron_bin.c
        scripts/tn_neuron_bin.h
        )

function (create_symlinks)
    # Do nothing if building in-source
    if (${CMAKE_CURRENT_BINARY_DIR} STREQUAL ${CMAKE_CURRENT_SOURCE_DIR})
        return()
    endif()

    foreach (path_file ${ARGN})
        get_filename_component(folder ${path_file} PATH)

        # Create REAL folder
        file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/${folder}")

        # Delete symlink if it exists
        file(REMOVE "${CMAKE_CURRENT_BINARY_DIR}/${path_file}")

        # Get OS dependent path to use in `execute_process`
        file(TO_NATIVE_PATH "${CMAKE_CURRENT_BINARY_DIR}/${path_file}" link)
        file(TO_NATIVE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/scripts/${path_file}" target)

        if (UNIX)
            set(command ln -s ${target} ${link})
        else()
            set(command cmd.exe /c mklink ${link} ${target})
        endif()

        execute_process(COMMAND ${command}
                RESULT_VARIABLE result
                ERROR_VARIABLE output)

        if (NOT ${result} EQUAL 0)
            message(FATAL_ERROR "Could not create symbolic link for: ${target} --> ${output}")
        endif()

    endforeach(path_file)
endfunction(create_symlinks)

set(SCRIPT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/scripts")

file(GLOB_RECURSE files RELATIVE ${SCRIPT_DIR} *.py *.dat *.rb)
create_symlinks(${files})


ADD_EXECUTABLE(NeMo  ${model_srcs})
if (${COMPILE_PYTHON})
    ADD_LIBRARY(NemoGen MODULE ${gen_srcs})
    find_file(TN_NEURON NAMES tn_neuron.h PATHS ${CMAKE_CURRENT_SOURCE_DIR}/neuro)
    ADD_CUSTOM_COMMAND(TARGET NemoGen POST_BUILD COMMAND ${PYBIN} build.py compiletn ${TN_NEURON} ${CMAKE_CURRENT_BINARY_DIR})
endif()
TARGET_LINK_LIBRARIES(NeMo ROSS m)




