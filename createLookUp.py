from Bio import SeqIO
import re
import os
import argparse

parser = argparse.ArgumentParser(description='Give it several fields, and it will create a tab-delimited lookup table')

parser.add_argument('-g', '--genbank',
    help="Genbank file to summarize",
    required=True)

parser.add_argument('-p', '--primary',
    default="protein_id",
    help="Primary qualifier" )

parser.add_argument('-s', '--secondary',
    default="gene_synonym,gene",
    help="Secondary qualifier(s)" )

parser.add_argument('-f', '--filter',
    default="",
    help="Use only secondary qualifiers that contain this field" )

args = parser.parse_args()

qualifiers = {}

# go through once to get all of the primary qualifiers, add to a dictionary of lists
for seq_record in SeqIO.parse(args.genbank, "genbank"):
    for feature in seq_record.features:
        for qualifierKey in feature.qualifiers:
            if qualifierKey == args.primary:
                for primaryID in feature.qualifiers[qualifierKey]:
                    qualifiers[primaryID] = []

#
for seq_record in SeqIO.parse(args.genbank, "genbank"):
    for feature in seq_record.features:
        primaryList = ""
        secondaryList = []
        for qualifierKey in feature.qualifiers:
            if qualifierKey == args.primary:
                primaryList = feature.qualifiers[qualifierKey]

            split = args.secondary.split(",")
            for secondary in split:
                if qualifierKey == secondary:
                    for secondSecondary in feature.qualifiers[qualifierKey]:
                        secondaryList.append(secondSecondary)

        for primary in primaryList:
            for secondary in secondaryList:
                qualifiers[primary].append(secondary)

#
for primary in qualifiers:
    for secondary in qualifiers[primary]:
        if args.filter in secondary:
            print(primary,secondary,sep="\t")
