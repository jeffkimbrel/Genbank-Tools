#! /usr/bin/env python

from Bio import SeqIO
import re
import os
import argparse
import datetime
import tools.gb

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description='XXX')

########## Required ############################################################

parser.add_argument('-g', '--genbank',
                    help="Genbank file to update",
                    required=True)
parser.add_argument('-p', '--prefix',
                    help="locus tag prefix",
                    default="lt_")
parser.add_argument('-a', '--accession',
                    help="Use accession instead of prefix? Overwrites -p option",
                    action="store_true")
parser.add_argument('-o', '--out',
                    help="output file name",
                    required=True)
args = parser.parse_args()

## MISC ########################################################################

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
currentCounter = 1

## LOOP THROUGH GENBANK ########################################################

for seq_record in SeqIO.parse(args.genbank, "genbank"):

    locus_tag_prefix = ""

    if args.accession == True:
        locus_tag_prefix = seq_record.annotations['accessions'][0] + "_"
        currentCounter = 1
    else:
        locus_tag_prefix = args.prefix

    # dna->DNA
    #seq_record.annotations['molecule_type'] = tools.gb.fixMoleculeType(seq_record.annotations['molecule_type'])

    # for IMG
    seq_record.id = seq_record.description

    ###### Update comments and version #########################################

    seq_record = tools.gb.addComment(seq_record, "=====" + timestamp + "=====")
    seq_record = tools.gb.addComment(seq_record, "program=createLocusTags.py")
    argsDict = vars(args)
    for arg in argsDict:
        seq_record = tools.gb.addComment(seq_record, (str(arg) + "=" + str(argsDict[arg])))

    seq_record = tools.gb.incrementVersion(seq_record, inc=True)

    ###### Standardize #########################################################

    new_features = []
    for feature in seq_record.features:
        if feature.type == 'source':
            new_features.append(feature)
        elif feature.type == 'fasta_record':
            new_features.append(feature)

        else:

            feature.qualifiers['locus_tag'] = locus_tag_prefix + str(currentCounter)
            currentCounter += 1
            new_features.append(feature)

    seq_record.features = new_features

    ## WRITE ###################################################################

    output_handle = open(args.out, "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
