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

def readHeader(fileName = "../neuro/tn_neuron.h", name="TN_MODEL"):
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
                if "}" in line:
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

if __name__ == '__main__':
    hdr = readHeader()
    print(hdr)
    with open('hdrs.csv','w') as csvfile:
        fieldnames = ['type', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for type,name in zip(hdr[0],hdr[1]):
            writer.writerow({'type': type, 'name':name})

