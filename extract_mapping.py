#! /usr/bin/env python

from Bio import SeqIO
import re
import os
import argparse

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(
    description='Extract features and annotations from a genbank file using flags')

parser.add_argument('-g', '--genbank',
                    help="Genbank file",
                    required=True)


args = parser.parse_args()

## LOOP ########################################################################

for seq_record in SeqIO.parse(args.genbank, "genbank"):
    for feature in seq_record.features:
        if feature.type == 'CDS':
            locus_tag = ""
            old_locus_tag = ""
            protein_id = ""
            for key in feature.qualifiers:
                if key == "locus_tag":
                    locus_tag = feature.qualifiers[key][0]
                if key == "old_locus_tag":
                    old_locus_tag = feature.qualifiers[key][0]
                if key == "protein_id":
                    protein_id = feature.qualifiers[key][0]
            print(locus_tag, protein_id, sep = "\t")

