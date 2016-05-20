from Bio import SeqIO
import re
import os
import argparse

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
            print(">"+str(feature.qualifiers[args.identifier][0])+"\n"+str(feature.qualifiers['translation'][0]))