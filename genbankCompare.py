#! /usr/bin/env python

from Bio import SeqIO
import re
import os
import argparse

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = 'Compares the different statistics of two genbank files')

parser.add_argument('-g', '--genbank',
    help="List of genbank files (spaces-separated)",
    nargs = '*',
    required=True)

parser.add_argument('-m', '--markdown',
    action = "store_true",
    help="Format table output for markdown" )

args = parser.parse_args()

## MISC ########################################################################

colSep = "\t"

if args.markdown == True:
    colSep = " | "

print("TYPE1", "TYPE2", sep = colSep, end = colSep)
for genbankFile in args.genbank:
    print(genbankFile, sep = colSep, end = colSep)
print()

if args.markdown == True:
    print("---", "---", sep = colSep, end = colSep)
    for genbankFile in args.genbank:
        print("---", sep = colSep, end = colSep)
    print()

featuresDict = {}
qualifierDict = {}
db_xrefDict = {}

## GENBANK #####################################################################

for genbankFile in args.genbank:

    featuresDict[genbankFile] = {}
    qualifierDict[genbankFile] = {}
    db_xrefDict[genbankFile] = {}

    for seq_record in SeqIO.parse(genbankFile, "genbank"):
        for feature in seq_record.features:
            featuresDict[genbankFile][feature.type] = featuresDict[genbankFile].get(feature.type, 0) + 1

            for qualifierKey in feature.qualifiers:

                if qualifierKey in qualifierDict[genbankFile]:
                    qualifierDict[genbankFile][qualifierKey] += feature.qualifiers[qualifierKey]
                else:
                    qualifierDict[genbankFile][qualifierKey] = feature.qualifiers[qualifierKey]

                ## DB_XREF #####################################################
                if qualifierKey == 'db_xref':
                    for key in feature.qualifiers[qualifierKey]:
                        value = key.split(":")

                        if value[0] in db_xrefDict[genbankFile]:
                            db_xrefDict[genbankFile][value[0]].append(value[0])
                        else:
                            db_xrefDict[genbankFile][value[0]] = [value[0]]

## FEATURES ####################################################################

uniqueFeatures = []

for genbankFile in sorted(featuresDict.keys()):
    for feature in featuresDict[genbankFile]:
        uniqueFeatures.append(feature)

uniqueFeatures = list(set(uniqueFeatures))

for feature in sorted(uniqueFeatures):
    print("FEATURE", feature, sep = colSep, end = colSep)
    for genbankFile in sorted(featuresDict.keys()):
        if feature in featuresDict[genbankFile]:
            print(featuresDict[genbankFile][feature], end = colSep, sep = colSep)
        else:
            print(0, end = colSep, sep = colSep)
    print()

## QUALIFIERS ##################################################################

uniqueQualifiers = []

for genbankFile in sorted(qualifierDict.keys()):
    for feature in qualifierDict[genbankFile]:
        uniqueQualifiers.append(feature)

uniqueQualifiers = list(set(uniqueQualifiers))

for qualifier in sorted(uniqueQualifiers):
    print("QUALIFIER", qualifier, sep = colSep, end = colSep)
    for genbankFile in sorted(qualifierDict.keys()):
        if qualifier in qualifierDict[genbankFile]:

            total = len(qualifierDict[genbankFile][qualifier])
            unique = len(list(set(qualifierDict[genbankFile][qualifier])))
            value = str(total) + " (" + str(unique) + ")"

            print(value, end = colSep, sep = colSep)
        else:
            print(0, end = colSep, sep = colSep)
    print()

## DB_XREF #####################################################################

uniqueDB = []

for genbankFile in sorted(db_xrefDict.keys()):
    for feature in db_xrefDict[genbankFile]:
        uniqueDB.append(feature)

uniqueDB = list(set(uniqueDB))

for db in sorted(uniqueDB):
    print("DB_XREF", db, sep = colSep, end = colSep)
    for genbankFile in sorted(db_xrefDict.keys()):
        if db in db_xrefDict[genbankFile]:

            total = len(db_xrefDict[genbankFile][db])
            unique = len(list(set(db_xrefDict[genbankFile][db])))
            value = str(total) + " (" + str(unique) + ")"

            print(value, end = colSep, sep = colSep)
        else:
            print(0, end = colSep, sep = colSep)
    print()
