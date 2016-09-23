//
// Created by Mark Plagge on 9/15/16.
//

#ifndef ROSS_TOP_TN_NEURON_BIN_H
#define ROSS_TOP_TN_NEURON_BIN_H

#include "../globals.h"
#include "../neuro/tn_neuron.h"
#include <stdlib.h>
#include <stdio.h>
//#include <Python.h>
//#include "../../../core/ross.h"

void *createFromData(bool* synapticConnectivity,
                                short* G_i,
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
                                uint64_t destGlobalID,
                                int destAxonID
);
//int main(int argc, char *argv[]);
#endif //ROSS_TOP_TN_NEURON_BIN_H
