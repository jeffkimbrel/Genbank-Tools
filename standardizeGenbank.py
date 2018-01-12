#! /usr/bin/env python

from Bio import SeqIO
import re
import os
import argparse
import datetime
from tools.gb import *

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

## OPTIONS

parser = argparse.ArgumentParser(description = 'Clean a genbank file')

parser.add_argument('-g', '--genbank',
    help = "Genbank file to update",
    required = True)

parser.add_argument('-l', '--locus',
    help = "locus tag prefix",
    required = True)

parser.add_argument('-p', '--pseudogenes',
    action = "store_true",
    help = "Allow pseudogenes to be included, default = NO")

parser.add_argument('-t', '--trna',
    action = "store_true",
    help = "Allow tRNA to be included, default = NO")

parser.add_argument('-r', '--rrna',
    action = "store_true",
    help = "Allow rRNA to be included, default = NO")

keeperQualifiers = ['protein_id', 'locus_tag', 'translation']

locusTagFields = ['gene', 'gene_synonym', 'locus_tag', 'old_locus_tag']

args = parser.parse_args()

def filterQualifiers(feature, keeperQualifiers):
    for qualifier in feature.qualifiers:
        if qualifier not in keeperQualifiers:
            feature.qualifiers[qualifier] = []
        else:
            feature.qualifiers[qualifier] = feature.qualifiers[qualifier]

    return(feature)





for seq_record in SeqIO.parse(args.genbank, "genbank"):

    # for IMG
    seq_record.id = seq_record.description

    seq_record = addComment(seq_record, (timestamp + " - Standardized " + args.genbank))
    seq_record = incrementVersion(seq_record)


    new_features = []
    for feature in seq_record.features:
        if feature.type == 'CDS':

            # search for locus tag
            locusTag = ""
            for qualifier in feature.qualifiers:
                if qualifier in locusTagFields:
                    #print(args.locus)
                    for potential in feature.qualifiers[qualifier]:
                        if str(args.locus) in potential:
                            locusTag = potential
            feature.qualifiers['locus_tag'] = [locusTag]

            # just for IMG genomes
            feature.qualifiers['protein_id'] = [locusTag]

            # remove all but the "keepers"
            feature = filterQualifiers(feature, keeperQualifiers)

            # print all (allow pseudogenes) or only print if all keepers are present
            if args.pseudogenes == False:
                allow = 1
                for qualifier in keeperQualifiers:
                    if qualifier not in feature.qualifiers:
                        allow = 0
                if allow == 1:
                    new_features.append(feature)
            else:
                new_features.append(feature)

        if feature.type == 'tRNA':
            if args.trna == True:
                feature = filterQualifiers(feature, keeperQualifiers)
                new_features.append(feature)

        if feature.type == 'rRNA':
            if args.rrna == True:
                feature = filterQualifiers(feature, keeperQualifiers)
                new_features.append(feature)

    seq_record.features = new_features

    ### Write to file
    output_handle = open(args.genbank+".cleaned_"+timestamp+".gbk", "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
