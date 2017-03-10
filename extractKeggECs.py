#! /usr/bin/env python

import re
import os
import argparse
import functions as f

parser = argparse.ArgumentParser(description='Extract EC numbers from a KEGG?KAAS output file')

parser.add_argument('-k', '--kaas',
    help="KEGG/KAAS File",
    required=True)

parser.add_argument('-v', '--verbose',
    action = "store_true",
    help="Print a bit more summary" )

args = parser.parse_args()
# convert map file to dictionary
mapDict = {}

mapFile = "/Users/jak/Dropbox/LLNL/Projects/Modeling/IA/kegg2EC.txt"
for line in open(mapFile, 'rt'):
    line = line.rstrip()
    ecList = re.findall(r"[0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+", line)
    ecList = f.cleanEC(ecList)

    split = line.split("\t")
    mapDict[split[0]] = ecList

# Process KAAS File
for line in open(args.kaas, 'rt'):
    line = line.rstrip()
    split = line.split("\t")

    if len(split) > 1:

        locus = split[0]
        ko = split[1]

        if args.verbose == True:
            if ko in mapDict:
                print(split[0], ko, sep = "\t", end = "\t")
                print(*mapDict[ko], sep = ";")
            else:
                print(split[0], ko, "Not Found", sep = "\t")
        else:
            if ko in mapDict:
                print(split[0], sep = "\t", end = "\t")
                print(*mapDict[ko], sep = ";")
