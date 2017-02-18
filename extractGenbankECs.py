from Bio import SeqIO
import os
import argparse
import functions as f

parser = argparse.ArgumentParser(description='Extract EC numbers from a genbank file')

parser.add_argument('-g', '--genbank',
    help="Genbank file path",
    required=True)

args = parser.parse_args()

for seq_record in SeqIO.parse(args.genbank, "genbank"):
    for feature in seq_record.features:
        if feature.type == 'CDS':

            # get locus/gene name
            locus = ""
            if 'locus_tag' in feature.qualifiers:
                locus = feature.qualifiers['locus_tag'][0]
            elif 'gene' in feature.qualifiers:
                locus = feature.qualifiers['gene'][0]

            # get functions
            EC_number = ""
            if 'EC_number' in feature.qualifiers:
                EC_number = feature.qualifiers['EC_number']
                #print("**",EC_number)

            ecList = f.cleanEC(EC_number)

            # print
            if len(ecList) > 0:
            #print(locus,function,sep="\t",end="\t")
                print(locus,end="\t")
                print(*ecList,sep=";")
