//
// Created by mplagge on 4/28/15.
//

#ifndef ROSS_TOP_MODEL_MAIN_H
#define ROSS_TOP_MODEL_MAIN_H
#include "models/neuron_model.h"
#include "models/synapse.h"
#include "assist.h"
#include "ross.h"
#include "spike_generator.h"
#include <stdio.h>

/** LP definition array.
 * simplified from tnt_main */



/** Variable holders for command lne params & external variables */
int NEURONS_IN_CORE = 4;
int SYNAPSES_IN_CORE = 8;
int CORES_IN_SIM = 2;
int THRESHOLD_MAX = 11;
int THRESHOLD_MIN = 5;
int SYNAPSE_WEIGHT_MAX= 10;
int SYNAPSE_WEIGHT_MIN= 5;
int DENDRITE_MIN= 1;
int DENDRITE_MAX= 1;
int DENDRITE_W_MIN=1;
int DENDRITE_W_MAX=2;
int CORE_SIZE;
float CLOCK_SPEED = 1;
//gen lag timer:
int GEN_LAG = 1000;
bool USE_OTHER_LEAKS = false;
bool USE_OTHER_RESET = false;
int MIN_LEAK = 0;
int MAX_LEAK = 10;
char *ALT_LEAK;
char *ALT_RESET;
int MIN_RESET = 0;
int MAX_RESET = 10;
int DEBUG_MODE = 0;
///// Ugly - maybe there's a better way to declare these?
//ROSS OPTIONS:
char* configFilePath;
bool isFile;
tw_stime lookahead = .00000000001;
int events_per_pe = 0;
int EXEC_MEMORY = 100000000;
int CLOCK_RATE = 10;
//Synapses and neuron max values (for off-by-one errors):
int tt_neurons = 0;
int tt_synapses = 0;
/** Generator Options */
bool GEN_ON = 1;
bool GEN_RND = 1;
int RND_MODE = 0;
unsigned int GEN_PROB = 50;
unsigned int GEN_FCT = 5;
int GEN_OUTBOUND = 4;

//for benchmark, using simplified options.8
const tw_optdef app_opt[] = {
        TWOPT_GROUP("Config File Settings"),
        TWOPT_FLAG("loadF", isFile, "Load a file?"),
        TWOPT_CHAR("cnf_file", configFilePath, "Network Config File Path -- In Network Config format."),
        TWOPT_GROUP("Non-File Configuration"),
        TWOPT_UINT("neurons", NEURONS_IN_CORE, "Neurons per core"),
        TWOPT_UINT("synapses", SYNAPSES_IN_CORE, "Synapses per core"),
        TWOPT_UINT("cores", CORES_IN_SIM, "Cores per PE"),
        TWOPT_UINT("th_min", THRESHOLD_MIN, "minimum threshold for neurons"),
        TWOPT_UINT("th_max", THRESHOLD_MAX, "maximum threshold for neurons"),
        TWOPT_UINT("wt_min", SYNAPSE_WEIGHT_MIN, "minimum synapse weight"),
        TWOPT_UINT("wt_max", SYNAPSE_WEIGHT_MAX, "maximum synapse wweight"),
        TWOPT_GROUP("Input Sim Generator Options"),
        TWOPT_FLAG("genon", GEN_ON, "Input Generator On"),
        TWOPT_FLAG("genrd", GEN_RND, "Use Random Input"),
        TWOPT_UINT("rndMd", RND_MODE, "Random gen mode. 0 is GE uniform. 1 is geometric. 2 is binomial. "),
        TWOPT_ULONG("prob", GEN_PROB, "Probability setting"),
        TWOPT_ULONG("ftr", GEN_FCT, "Probability or Lambda for geometric or binomial option."),
        TWOPT_ULONG("genout", GEN_OUTBOUND,
                    "Number of outbound connections for generator (Set <= number of synapses per core."),
        TWOPT_GROUP("Misc. Settings"),
        TWOPT_FLAG("debug", DEBUG_MODE, "Enable debug output"),
        TWOPT_ULONG("events", events_per_pe, "Events per PE"),
        TWOPT_STIME("lh", lookahead, "Lookahead Setting"),
        {TWOPT_END()}
};

extern tw_lptype model_lps[];
void pre_run();
//Function headers through the main function.
void neuron_event(neuronState *s, tw_bf *CV, Msg_Data *M, tw_lp *lp);

void synapse_event(synapseState *s, tw_bf *, Msg_Data *M, tw_lp *lp);

void neuron_init(neuronState *s, tw_lp *lp);

void synapse_init(synapseState *s, tw_lp *lp);


//helper functions for expansion of functionality
void setSynapseWeight(neuronState *s, tw_lp *lp, int synapseID);


//reverse functions:
void neuron_reverse(neuronState *, tw_bf *, Msg_Data *, tw_lp *);

void synapse_reverse(neuronState *, tw_bf *, Msg_Data *, tw_lp *);


//neuron management functions
void synapseIn(int synapseID, neuronState *s);

void calculateThreshold(int synapseID, neuronState *s);

void checkFire(int synapseID, neuronState *s);

//functions for the end of the simulation:
void neuron_final(neuronState *s, tw_lp *lp);

void synapse_final(synapseState *s, tw_lp *lp);

//functions for input simulation/handling:
void gen_init(spikeGenState *gen_state,tw_lp *lp);
void gen_pre(spikeGenState *gen_state,tw_lp *lp);
void gen_event(spikeGenState *gen_state,tw_lp *lp);
void gen_reverse(spikeGenState *gen_state,tw_lp *lp);
void gen_final(spikeGenState *gen_state,tw_lp *lp);

//Mapping funtions

/** Given a global ID, return the core number */
_regionIDType getCoreID(gid_t global);
_regionIDType getLocalID(gid_t global);
void getLocalIDs(gid_t global, _regionIDType * core, _regionIDType *local );
gid_t getGlobalID(_regionIDType core, _regionIDType local);
#endif //ROSS_TOP_MODEL_MAIN_H