//
// Created by Mark Plagge on 9/15/16.
//

#include "tn_neuron_bin.h"

//int main(int argc, char *argv[]) {
//    PyObject *pName, *pModule, *pDict, *pFunc, *pValue;
//
//}

void *createFromData(bool *synapticConnectivity,
                     short *G_i,
                     short sigma[4],
                     short S[4],
                     bool b[4],
                     bool epsilon,
                     short sigma_l,
                     short lambda,
                     bool c,
                     uint32_t alpha,
                     uint32_t beta,
                     short TM,
                     short VR,
                     short sigmaVR,
                     short gamma,
                     bool kappa,
                     int signalDelay,
                     int destAxonID,
                     int destAxonCore,
                     int neuronID,
                     int neuronCore
) {
    tn_neuron_state *st;


    return st;
}