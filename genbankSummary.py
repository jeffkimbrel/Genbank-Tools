#! /usr/bin/env python


from Bio import SeqIO
import re
import os
import argparse

# RAST output by default has an incorrect header which leads to a BioPython warning. This will suppress all warnings.
import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)
#

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description='Summarize the contents of a genbank file or record')

parser.add_argument('-g', '--genbank',
    help="Genbank file to summarize",
    required=True)

parser.add_argument('-i', '--id',
    default="all",
    help="Limit to only the record with this ID" )

parser.add_argument('-c', '--combine',
    action = "store_true",
    help="Combine all records into a single summary" )

parser.add_argument('-m', '--markdown',
    action = "store_true",
    help="Format table output for markdown" )

args = parser.parse_args()

## MISC ########################################################################

features = {}
qualifiers = {}
db_xref = {}

colSep = "\t"

if args.markdown == True:
    colSep = " | "

print("RECORD", "TYPE1", "TYPE2", "COUNT", "UNIQUE", sep = colSep)

if args.markdown == True:
    print("--- | --- | --- | --- | ---")

## LOOP ########################################################################

for seq_record in SeqIO.parse(args.genbank, "genbank"):

    if args.id == "all" or args.id == str(seq_record.id):

## INCREASE COUNT OF FEATURE TYPE IN features DICTIONARY
        for feature in seq_record.features:
            features[feature.type] = features.get(feature.type, 0) + 1

## GET QUALIFIERS OF FEATURES
            for qualifierKey in feature.qualifiers:
                for qualifierValue in feature.qualifiers[qualifierKey]:

                    if qualifierKey in qualifiers: ## IF SO, THEN APPEND QUALIFIER VALUE TO LIST
                        qualifiers[qualifierKey].append(qualifierValue)
                    else: # OTHERWISE, ADD NEW
                        qualifiers[qualifierKey] = [qualifierValue]

## GET DB_XREF TYPES
                    if qualifierKey == 'db_xref':
                        db = qualifierValue.split(":")

                        if db[0] in db_xref: ## IF SO, THEN APPEND QUALIFIER VALUE TO LIST
                            db_xref[db[0]].append(db[1])
                        else: # OTHERWISE, ADD NEW
                            db_xref[db[0]] = [db[1]]

## DISPLAY IF -c FLAG IS FALSE
        if args.combine == False:
            for featureType in sorted(features.keys()):
                print(seq_record.id, "feature", featureType, str(features[featureType]), sep = colSep)

            for qualifierType in sorted(qualifiers.keys()):
                unique = str(len(list(set(qualifiers[qualifierType]))))
                print(seq_record.id, "qualifier", qualifierType, str(len(qualifiers[qualifierType])), unique, sep = colSep)

            for dbType in sorted(db_xref.keys()):
                unique = str(len(list(set(db_xref[dbType]))))
                print(seq_record.id, "db_xref", dbType, str(len(db_xref[dbType])), unique, sep = colSep)

## RESET DICTIONARIES
            features = {}
            qualifiers = {}
            db_xref = {}

## DISPLAY IF -c FLAG IS TRUE
if args.combine == True:
    for featureType in sorted(features.keys()):
        print(str(args.genbank), "feature", featureType, str(features[featureType]), sep = colSep)

    for qualifierType in sorted(qualifiers.keys()):
        unique = str(len(list(set(qualifiers[qualifierType]))))
        print(str(args.genbank), "qualifier", qualifierType, str(len(qualifiers[qualifierType])), unique, sep = colSep)

    for dbType in sorted(db_xref.keys()):
        unique = str(len(list(set(db_xref[dbType]))))
        print(str(args.genbank), "db_xref", dbType, str(len(db_xref[dbType])), unique, sep = colSep)
