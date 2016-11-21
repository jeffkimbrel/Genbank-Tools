import re
import os
import argparse

parser = argparse.ArgumentParser(description='Extract Brenda and EFICAz EC numbers from PSAT Output')

parser.add_argument('-p', '--psat',
    help="Path to psat output",
    required=True)

args = parser.parse_args()

psatFile = open(args.psat, 'rt')

##### FUNCTIONS #####
def cleanEC(ecList):

    completeList = []
    incompleteList = []

    for ec in ecList:
        if '-' in ec:
            incompleteList.append(ec)
        else:
            completeList.append(ec)

    completeList = list(set(completeList))
    incompleteList = list(set(incompleteList))

    for incompleteEC in list(incompleteList): # iterate through a copy
        for completeEC in completeList:
            if completeEC.startswith(incompleteEC.rstrip('.-')):

                #print(completeEC,incompleteEC,sep="\t")
                if incompleteEC in incompleteList:
                    incompleteList.remove(incompleteEC)

    ecListFinal = incompleteList + completeList

    return(ecListFinal)


ecDict = {}

while True:
    line = psatFile.readline()
    line = line.rstrip()

    if not line.lstrip().startswith('#'):
        split = line.split('\t')
        if len(split) > 2:
            nameSplit = split[2].split('/')
            locus_tag = nameSplit[1]

            if locus_tag not in ecDict:
                ecDict[locus_tag] = {"BRENDA" : [], "EFICAz" : []}

            if split[3] != "":
                ec = split[3]

                if len(split) > 6 and split[6] != "":
                    ecDict[locus_tag]["EFICAz"].append(ec)

                if len(split) > 7 and split[7] != "":
                    ecDict[locus_tag]["BRENDA"].append(ec)

    if not line:
        break

print("LOCUS_TAG","EFICAz","BRENDA","NR")

for locus_tag in sorted(ecDict.keys()):
    eficaz = cleanEC(ecDict[locus_tag]["EFICAz"])
    brenda = cleanEC(ecDict[locus_tag]["BRENDA"])

    both = eficaz + brenda
    both = cleanEC(both)

    if eficaz == []:
        eficaz = ["NA"]
    if both == []:
        both = ["NA"]
    if brenda == []:
        brenda = ["NA"]

    if "NA" not in eficaz or "NA" not in brenda or "NA" not in both:
        print(locus_tag,end="\t")
        print(*eficaz,sep=";",end="\t")
        print(*brenda,sep=";",end="\t")
        print(*both,sep=";")

    #print(locus_tag,len(eficaz),len(brenda),len(both),sep="\t")
