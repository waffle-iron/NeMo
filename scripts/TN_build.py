from cffi import FFI
import os

ffi = FFI()
# TODO : Set this to load globals.h (potentially eliminating the need for these typedefs
ffi.set_source("_tn_neuron",None)
ffi.cdef("""

typedef uint_fast16_t id_type; //!< id type is used for local mapping functions - there should be $n$ of them depending on CORE_SIZE
typedef int32_t volt_type; //!< volt_type stores voltage values for membrane potential calculations
typedef int64_t weight_type;//!< seperate type for synaptic weights.
typedef uint32_t thresh_type;//!< Type for weights internal to the neurons.
typedef uint16_t random_type;//!< Type for random values in neuron models.

typedef uint64_t size_type; //!< size_type holds sizes of the sim - core size, neurons per core, etc.

typedef uint64_t stat_type;
    void * createFromData(id_type coreID, id_type nID,
                      bool* synapticConnectivity,
                      short* G_i, short sigma[4], short S[4],
                      bool b[4], bool epsilon, short sigma_l, short lambda,
                      bool c, uint32_t alpha, uint32_t beta, short TM, short VR,
                      short sigmaVR, short gamma, bool kappa,
                       int signalDelay,
                      uint64_t destGlobalID, int destAxonID);
""")
# TODO: create setup.py or integration with cmake so this is automated.
C = ffi.dlopen('libNemoGen.so')

# ffibuilder.set_source("_tnStruct",
#                       """
#                       #include "tn_neuron_bin.h"
#                       """,
#                       libraries=[])
# lib = ffibuilder.dlopen("/Users/markplagge/Dev/build/models/NeMo/libNemoGen.so")


if __name__ == '__main__':
    ffi.compile(verbose=True)