#! /usr/bin/env python

import re
import os
import sys
from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
import argparse
import datetime
import tools.gb
import tools.anno

## MISC ########################################################################

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = 'Splits RFAM into annotations with and without existing locus_tags')

parser.add_argument('-r', '--rfam',
    help="RFAM .tblout File",
    required=True)

parser.add_argument('-g', '--genbank',
    help="Genbank file with existing annotation information",
    required=True)

parser.add_argument('-l', '--locus_tag',
    help="Append this to new misc_RNA features (automatically adds the '_')",
    required=True)

parser.add_argument('-o', '--out',
    help = "Output File",
    required = True)

parser.add_argument('-c', '--additionalComment',
    required = False,
    default = "added RFAM results to .gbk",
    help = "Add to the comment line, default = NO")

args = parser.parse_args()

## PROCESS RFAM ################################################################

rfamResults = {}

lines = [line.strip() for line in open(args.rfam)]

counter = 0

for line in lines:
    if not line.lstrip().startswith('#'):
        counter += 1
        line = line.rstrip()
        split = line.split()

        start = int(split[9])
        stop = int(split[10])

        if start > stop:
            start = int(split[10])
            stop = int(split[9])

        strand = -1

        if split[11] == "+":
            strand = 1

        rfamResults[counter] = {'id' : counter, 'name' : split[1], 'accession' : split[2], 'contig' : split[3], 'clan' : split[5], 'start' : start, 'stop' : stop, 'strand' : strand, 'completed' : 0}

## PROCESS GENBANK #############################################################

for seq_record in SeqIO.parse(args.genbank, "genbank"):
    ## for IMG
    seq_record.id = seq_record.description

    ###### Update comments and version #########################################

    seq_record = tools.gb.addComment(seq_record, "=====" + timestamp + "=====")
    seq_record = tools.gb.addComment(seq_record, "program=updateGenbankWithRFAM.py")
    argsDict = vars(args)
    for arg in argsDict:
        seq_record = tools.gb.addComment(seq_record, (str(arg) + "=" + str(argsDict[arg])))

    seq_record = tools.gb.incrementVersion(seq_record)

    ## NOW DO RFAM

    for rf in rfamResults:
        if rfamResults[rf]['contig'] == seq_record.name:
            seq_record.features.append(SeqFeature(
                FeatureLocation(
                    rfamResults[rf]['start'],
                    rfamResults[rf]['stop'],
                    strand=rfamResults[rf]['strand']
                ),
                type="misc_RNA",
                qualifiers = {
                    "product" : [rfamResults[rf]['name']],
                    "RNA_Class_ID" : [rfamResults[rf]['accession']],
                    "RNA_Clan_ID" : [rfamResults[rf]['clan']],
                    "locus_tag" : [args.locus_tag + "_" + str(rfamResults[rf]['id'])]
                }

            ))
            rfamResults[rf]['completed'] = 1
            print(seq_record.features[-1])



    ## WRITE ###################################################################

    output_handle = open(args.out, "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
