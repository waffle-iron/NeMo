import re

import csv
#Patterns:
bad = [re.compile("(\s+\/\/)")]
comment = re.compile("/\*[^*]*\*+(?:[^/*][^*]*\*+)*/")
scomment = re.compile("//.*?\n")
word = re.compile("([\S]+)")
def formatCleanHeader(header):
    inDef = True

    header = header.replace('\n','')
    matches = word.findall(header)

    name = [m[:-1] for m in matches if m.endswith(';')]
    value = [m for m in matches if not m.endswith((';'))]



    return value,name

def readHeader(fileName = "../neuro/tn_neuron.h", name="TN_MODEL",typedefname="tn_neuron_state"):
    inStruct = False

    def lineF(mode,line):
        return {
            'in': 1,
            'out': 2
        }

    def lineValidate(line):
        good = True
        # for p in bad:
        #     r = p.search(line)
        #     if r is not None:
        #         good = False

        return good




    with open(fileName, 'r', encoding="utf-8") as f:
        structDef = ""
        for line in f.readlines():
            if inStruct:
                if typedefname in line:
                    inStruct = False
                elif lineValidate(line):
                    structDef += line


            if name in line:
                inStruct = True
        structDef= structDef.lstrip()
        structDef=comment.sub('',structDef)
        structDef=scomment.sub('',structDef)
        #print(structDef)
        structDef = formatCleanHeader(structDef)
        return structDef
def getStruct(fileName = "../neuro/tn_neuron.h", name="TN_MODEL", typedefname="tn_neuron_state"):

    inStruct = False

    with open(fileName, 'r', encoding='utf-8') as f:
        structDef = ""
        for line in f.readlines():
            if inStruct:
                structDef += line
                if typedefname in line:
                    inStruct = False

            if name in line:
                inStruct = True
                structDef += line

    return structDef

def saveStruct(fileName = "../neuro/tn_neuron.h", name="TN_MODEL", typedefName="tn_neuron_state", saveName="tn_struct.txt"):
    structDef = getStruct(fileName=fileName, name=name, typedefname=typedefName)

    with open(saveName, 'w', encoding='utf-8') as f:
        f.write(structDef)


def tnMain(tn_header,cwd='.'):
    hdr = readHeader(fileName=tn_header)
    print(hdr)
    with open(cwd + '/hdrs.csv','w') as csvfile:
        fieldnames = ['type', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for type,name in zip(hdr[0],hdr[1]):
            writer.writerow({'type': type, 'name':name})

    saveStruct(fileName=tn_header, saveName=cwd + "/tn_struct.txt")

if __name__ == '__main__':

    tnMain()
