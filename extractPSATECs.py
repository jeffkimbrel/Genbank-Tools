#! /usr/bin/env python

import re
import os
import argparse
import functions as f

parser = argparse.ArgumentParser(description='Extract Brenda and EFICAz EC numbers from PSAT Output')

parser.add_argument('-p', '--psat',
    help="Path to psat output",
    required=True)

parser.add_argument('-v', '--verbose',
    action = "store_true",
    help="Print a bit more summary" )

args = parser.parse_args()

psatFile = open(args.psat, 'rt')

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

#print("LOCUS_TAG","EFICAz","BRENDA","NR",sep="\t")

for locus_tag in sorted(ecDict.keys()):
    eficaz = ecDict[locus_tag]["EFICAz"]
    brenda = ecDict[locus_tag]["BRENDA"]

    eficaz = f.cleanEC(eficaz)
    brenda = f.cleanEC(brenda)

    both = eficaz + brenda
    both = f.cleanEC(both)

    if eficaz == []:
        eficaz = ["NA"]
    if both == []:
        both = ["NA"]
    if brenda == []:
        brenda = ["NA"]

    if "NA" not in eficaz or "NA" not in brenda or "NA" not in both:
        print(locus_tag,end="\t")

        if args.verbose == True:
            print(*eficaz,sep=";",end="\t")
            print(*brenda,sep=";",end="\t")

        print(*both,sep=";")
