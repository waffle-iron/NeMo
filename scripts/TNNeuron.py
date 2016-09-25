"""
Contains a class/struct that represents a TN Neuron.
"""
import numpy as np
from cffi import FFI
import json
import os
from collections import OrderedDict


x = os.getcwd()
import sys

sys.path.append(x)
from _tn_neuron import ffi

"""
Typedef ref:
typedef uint_fast16_t id_type; //!< id type is used for local mapping functions - there should be $n$ of them depending on CORE_SIZE
typedef int32_t volt_type; //!< volt_type stores voltage values for membrane potential calculations
typedef int64_t weight_type;//!< seperate type for synaptic weights.
typedef uint32_t thresh_type;//!< Type for weights internal to the neurons.
typedef uint16_t random_type;//!< Type for random values in neuron models.

typedef uint64_t size_type; //!< size_type holds sizes of the sim - core size, neurons per core, etc.

typedef uint64_t stat_type;
/**@}*/

Struct:
typedef struct TN_MODEL {
  // 64
  tw_stime
      lastActiveTime;
  tw_stime lastLeakTime;
  tw_lpid outputGID;
  // stat_type fireCount; //!< count of this neuron's output
  stat_type rcvdMsgCount;  //!<  The number of synaptic messages received.
  stat_type SOPSCount;     //!<  A count for SOPS calculation
  volt_type membranePotential;  //!< current "voltage" of neuron, \f$V_j(t)\f$.
  thresh_type posThreshold;     //!< neuron's threshold value 𝛼
  thresh_type negThreshold;     //!< neuron's negative threshold, 𝛽
  id_type dendriteLocal;  //!< Local ID of the remote dendrite -- not LPID, but
  random_type drawnRandomNumber;  //!<When activated, neurons draw a new random
  random_type
      thresholdPRNMask; /**!< The neuron's random threshold mask - used for
  id_type myCoreID;  //!< Neuron's coreID
  id_type myLocalID;  //!< my local ID - core wise. In a 512 size core, neuron 0
  short largestRandomValue;
  short lambda;  //!< leak weight - \f$𝜆\f$ Leak tuning parameter - the leak
  short int resetMode;     //!< Reset mode selection. Valid options are 0,1,2 .
  volt_type resetVoltage;  //!< Reset voltage for reset params, \f$R\f$.
  short sigmaVR;           //!< reset voltage - reset voltage sign
  short encodedResetVoltage;  //!< encoded reset voltage - VR.
  short omega;                //!<temporary leak direction variable
  char *neuronTypeDesc;  //!< a debug tool, contains a text desc of the neuron.
  char sigma_l;          //!< leak sign bit - eqiv. to σ
  unsigned char delayVal;  //!<@todo: Need to fully implement this - this value
  bool firedLast;
  bool heartbeatOut;
  bool isSelfFiring;
  bool epsilon;  //!<epsilon function - leak reversal flag. from the paper this
  bool c;        //!< leak weight selection. If true, this is a stochastic leak
  bool kappa;  //!<Kappa or negative reset mode. From the paper's ,\f$𝜅_j\f$,
  bool canGenerateSpontaniousSpikes;
  char axonTypes[512];
  char synapticWeight[4];
  bool synapticConnectivity[512];
  /** stochastic weight mode selection. $b_j^{G_i}$ */
  bool weightSelection[4];
} tn_neuron_state;

"""

"""Create Neuron Ref:
id_type coreID, id_type nID,
                      bool synapticConnectivity[NEURONS_IN_CORE],
                      short G_i[NEURONS_IN_CORE],
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
                      tn_neuron_state* n,
                      int signalDelay,
                      uint64_t destGlobalID,
                      int destAxonID

"""

"""CREATE FROM ARGS REF:
 void * createFromData(void *createFromData(bool *synapticConnectivity,
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
                     int neuronCore);
                          """

lib = ffi.dlopen("libNemoGen.so")


class TNNeuron(object):
    coreID = 0
    nID = 0
    synapticConnectivity = []
    G_i = []
    sigma = []
    S = []
    b = []
    epsilon = 0
    sigma_l = 0
    lmbda = 0
    c = False
    alpha = 0
    beta = 0
    TM = 0
    VR = 0
    sigmaVR = 0
    gamma = 0
    signalDelay = 0
    destAxonID = 0
    destAxonCore = 0
    neuronID = 0
    neuronCore = 0

    objRef = ""

    def __init__(self,**kwargs):
        vs = vars(self)
        for key in kwargs.keys():
            vs[key] = kwargs[key]
        self.createObj()

    # def __init__(self, **kwargs):
    #     for key in kwargs:
    #         self.key = kwargs[key]


    def createObj(self):
         self.objRef = lib.createFromData(self.CoreID, self.nID, self.synapticConnectivity, self.G_i, self.sigma,
                                          self.S, self.b, self.epsilon, self.sigma_l, self.lmbda, self.c, self.alpha,
                                          self.beta, self.TM, self.VR, self.sigmaVR, self.gamma, self.kappa,
                                          self.signalDelay,
                                          self.destGlobalID, self.destAxonID, self.destAxonCore, self.neuronID,
                                          self.neuronCore)
    def to_dict(self):
        return vars(self)


