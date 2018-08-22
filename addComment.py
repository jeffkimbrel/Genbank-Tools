#! /usr/bin/env python

from Bio import SeqIO
from Bio.GenBank import RecordParser
import re
import os
import argparse
import datetime
import tools.gb

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = 'Add a comment to a genbank file')

########## Required ############################################################

parser.add_argument('-g', '--genbank',
    help = "Genbank file to update",
    required = True)
parser.add_argument('-c', '--comment',
    help = "comment",
    required = True)
parser.add_argument('-o', '--out',
    help = "out",
    required = True)
parser.add_argument('-v', '--incrementVersion',
    action = "store_false",
    help = "Increase version?, default = YES")

args = parser.parse_args()

## MISC ########################################################################

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

## LOOP THROUGH GENBANK ########################################################

for seq_record in SeqIO.parse(args.genbank, "genbank"):

    # dna->DNA
    seq_record.annotations['molecule_type'] = tools.gb.fixMoleculeType(seq_record.annotations['molecule_type'])

    ## for IMG
    seq_record.id = seq_record.description

    ## Update comments and version #############################################

    seq_record = tools.gb.addComment(seq_record, "=====" + timestamp + "=====")
    seq_record = tools.gb.addComment(seq_record, "program=addComment.py")
    argsDict = vars(args)
    for arg in argsDict:
        seq_record = tools.gb.addComment(seq_record, (str(arg) + "=" + str(argsDict[arg])))

    if args.incrementVersion == True:
        seq_record = tools.gb.incrementVersion(seq_record)

    ## WRITE ###################################################################

    output_handle = open(args.out, "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
