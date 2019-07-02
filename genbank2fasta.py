from Bio import SeqIO
import re
import os
import argparse
import sys

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description='Create .faa file from a genbank record')

parser.add_argument('-g', '--genbank',
                    help="Genbank file to summarize",
                    required=True)

parser.add_argument('-i', '--identifier',
                    default="locus_tag",
                    help="Which genbank identifier should be the fasta header")

parser.add_argument('-a', '--amino',
                    default=None,
                    help="Write amino acid fasta file",
                    required=False)

parser.add_argument('-n', '--nucleo',
                    default=None,
                    help="Write nucleic acid fasta file",
                    required=False)

args = parser.parse_args()

if args.amino != None:
    aa_file = open(args.amino, 'w')

if args.nucleo != None:
    nt_file = open(args.nucleo, 'w')

## LOOP ########################################################################

for seq_record in SeqIO.parse(args.genbank, "genbank"):
    for feature in seq_record.features:
        if feature.type == 'CDS':
            id = feature.qualifiers[args.identifier][0]
            if id == "":
                print("ERROR: NO HEADER FOUND: ",
                      feature.qualifiers['translation'][0], file=sys.stderr)

            else:
                if args.amino != None:
                    if 'translation' in feature.qualifiers:
                        aa = feature.qualifiers['translation'][0]
                        aa_file.write(">" + id + "\n" + aa + "\n")

                if args.nucleo != None:
                    nt = str(feature.location.extract(seq_record).seq)
                    nt_file.write(">" + id + "\n" + nt + "\n")

## CLOSE FILES #################################################################

if args.amino != None:
    aa_file.close()

if args.nucleo != None:
    nt_file.close()
