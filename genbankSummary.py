from Bio import SeqIO
import re
import os
import argparse

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

args = parser.parse_args()

features = {}
qualifiers = {}
db_xref = {}

print("RECORD","TYPE1","TYPE2","COUNT","UNIQUE",sep="\t")

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
            for featureType in features:
                print(seq_record.id,"feature",featureType,str(features[featureType]),sep="\t")

            for qualifierType in qualifiers:
                unique = str(len(list(set(qualifiers[qualifierType]))))
                print(seq_record.id,"qualifier",qualifierType,str(len(qualifiers[qualifierType])),unique,sep="\t")

            for dbType in db_xref:
                unique = str(len(list(set(db_xref[dbType]))))
                print(seq_record.id,"db_xref",dbType,str(len(db_xref[dbType])),unique,sep="\t")

## RESET DICTIONARIES
            features = {}
            qualifiers = {}
            db_xref = {}

## DISPLAY IF -c FLAG IS TRUE
if args.combine == True:
    for featureType in features:
        print("all","feature",featureType,str(features[featureType]),sep="\t")

    for qualifierType in qualifiers:
        unique = str(len(list(set(qualifiers[qualifierType]))))
        print("all","qualifier",qualifierType,str(len(qualifiers[qualifierType])),unique,sep="\t")

    for dbType in db_xref:
        unique = str(len(list(set(db_xref[dbType]))))
        print("all","db_xref",dbType,str(len(db_xref[dbType])),unique,sep="\t")
