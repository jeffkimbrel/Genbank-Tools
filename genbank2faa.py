from Bio import SeqIO
import re
import os
import argparse
import sys

parser = argparse.ArgumentParser(description='Create .faa file from a genbank record')

parser.add_argument('-g', '--genbank',
    help="Genbank file to summarize",
    required=True)

parser.add_argument('-i', '--identifier',
    default="locus_tag",
    help="Which genbank identifier should be the fasta header" )

args = parser.parse_args()

for seq_record in SeqIO.parse(args.genbank, "genbank"):
    for feature in seq_record.features:
        if 'translation' in feature.qualifiers:
            if feature.qualifiers[args.identifier][0] == "":
                print("ERROR: NO HEADER FOUND: ",feature.qualifiers['translation'][0],file=sys.stderr)
            else:
                print(">"+str(feature.qualifiers[args.identifier][0])+"\n"+str(feature.qualifiers['translation'][0]))
