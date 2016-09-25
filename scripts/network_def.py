import TNNeuron
import json,jsonschema

class Core(object):
    neurons = []

    def __init__(self, coreID):
        self.coreID = coreID

    def serialize(self):
        nstruct = {}
        i = 0
        for n in self.neurons:
            nstruct["neuron" + str(i)] = n.to_dict()

        core = {}
        core["ID"] = self.coreID
        core["neurons"] = nstruct

        return core


class networkLayout(object):
    cores = 10
    neuronsInCore = 256

    