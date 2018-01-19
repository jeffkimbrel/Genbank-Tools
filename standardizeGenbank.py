#! /usr/bin/env python

from Bio import SeqIO
import re
import os
import argparse
import datetime
import tools.gb

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = 'Clean a genbank file')

########## Required ############################################################

parser.add_argument('-g', '--genbank',
    help = "Genbank file to update",
    required = True)
parser.add_argument('-l', '--locus',
    help = "locus tag prefix",
    required = True)

########## Optional ############################################################

parser.add_argument('-t', '--trna',
    action = "store_true",
    help = "Allow tRNA to be included, default = NO")
parser.add_argument('-r', '--rrna',
    action = "store_true",
    help = "Allow rRNA to be included, default = NO")

args = parser.parse_args()

## MISC ########################################################################

keeperQualifiers = ['protein_id', 'locus_tag', 'translation']
locusTagFields = ['gene', 'gene_synonym', 'locus_tag', 'old_locus_tag']
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

## FUNCTIONS ###################################################################

def filterQualifiers(feature, keeperQualifiers):
    for qualifier in feature.qualifiers:
        if qualifier not in keeperQualifiers:
            feature.qualifiers[qualifier] = []
        else:
            feature.qualifiers[qualifier] = feature.qualifiers[qualifier]

    return(feature)

## LOOP THROUGH GENBANK ########################################################

for seq_record in SeqIO.parse(args.genbank, "genbank"):

    ## for IMG
    seq_record.id = seq_record.description

    ###### Update comments and version #########################################
    seq_record = tools.gb.addComment(seq_record, "=====" + timestamp + "=====")
    seq_record = tools.gb.addComment(seq_record, "program=standardizeGenbank.py")
    argsDict = vars(args)
    for arg in argsDict:
        seq_record = tools.gb.addComment(seq_record, (str(arg) + "=" + str(argsDict[arg])))

    seq_record = tools.gb.incrementVersion(seq_record, inc = False)

    ###### Standardize #########################################################
    new_features = []
    for feature in seq_record.features:
        if feature.type == 'source':
            new_features.append(feature)

        elif feature.type == 'CDS':

            ## search for locus tag
            locusTag = ""
            for qualifier in feature.qualifiers:
                if qualifier in locusTagFields:
                    #print(args.locus)
                    for potential in feature.qualifiers[qualifier]:
                        if str(args.locus) in potential:
                            locusTag = potential
            feature.qualifiers['locus_tag'] = [locusTag]

            ## just for IMG genomes
            feature.qualifiers['protein_id'] = [locusTag]

            ## remove all but the "keepers"
            feature = filterQualifiers(feature, keeperQualifiers)

            new_features.append(feature)

        elif feature.type == 'tRNA':
            if args.trna == True:
                feature = filterQualifiers(feature, keeperQualifiers)
                new_features.append(feature)

        elif feature.type == 'rRNA':
            if args.rrna == True:
                feature = filterQualifiers(feature, keeperQualifiers)
                new_features.append(feature)

    seq_record.features = new_features

    ## WRITE ###################################################################
    output_handle = open(args.genbank+".cleaned.gbk", "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
