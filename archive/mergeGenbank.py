#! /usr/bin/env python

from Bio import SeqIO
import re
import os
import argparse
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

## OPTIONS

parser = argparse.ArgumentParser(description='Merge CDS qualifiers of a secondary (-s) Genbank file into a Master (-m)')

parser.add_argument('-m', '--master',
    help="Master genbank file",
    required=True)

parser.add_argument('-s', '--secondary',
    help="Genbank file to merge into master",
    required=True)

parser.add_argument('-f', '--folder',
    help="Output folder, defaults to mergedOutput + timestamp",
    default="mergedOutput_"+timestamp)

args = parser.parse_args()

masterGenbankFH = args.master
secondaryGenbankFH = args.secondary
outputFolder = args.folder

print("\nOUTPUT FOLDER: "+outputFolder+"\n")

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

##
for masterGenbank in SeqIO.parse(masterGenbankFH, "genbank"):
    masterLength = len(masterGenbank.seq)
    print("ID: "+masterGenbank.id+"\nLENGTH: "+str(masterLength))

    secondaryQualifiers = {}

    ## SAVE SECONDARY FEATURES/QUALIFIERS FROM SOURCES OF SAME LENGTH
    for secondaryGenbank in SeqIO.parse(secondaryGenbankFH, "genbank"):
        secondaryLength = len(secondaryGenbank.seq)

        if secondaryLength == masterLength:

            ## loop through features
            for secondaryRecord in secondaryGenbank.features:
                if secondaryRecord.type == 'CDS':
                    secondaryQualifiers[str(secondaryRecord.location)] = secondaryRecord.qualifiers

    ## NOW GO THROUGH MASTER FEATURES, AND ADD SECONDARY QUALIFIERS
    for masterRecord in masterGenbank.features:
        if masterRecord.type == 'CDS':
            if str(masterRecord.location) in secondaryQualifiers:

                ## COMBINE TWO DICTIONARIES
                combinedQualifiers = masterRecord.qualifiers
                for key in secondaryQualifiers[str(masterRecord.location)]:

                    if key in combinedQualifiers:
                        for qualifier in secondaryQualifiers[str(masterRecord.location)][key]:
                            combinedQualifiers[key].append(qualifier)
                    else:
                        combinedQualifiers[key] = secondaryQualifiers[str(masterRecord.location)][key]


                ## REMOVE QUALIFIER REDUNDANCY
                for qualifier in combinedQualifiers:
                    combinedQualifiers[qualifier] = list(set(combinedQualifiers[qualifier]))

                masterRecord.qualifiers = combinedQualifiers



    ### Write to file
    output_handle = open(outputFolder+"/merged.gbk", "a")
    SeqIO.write(masterGenbank, output_handle, "genbank")
    output_handle.close()
