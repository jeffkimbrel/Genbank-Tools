from Bio import SeqIO
import re
import os
import argparse
import functions as f

# RAST output by default has an incorrect header which leads to a BioPython warning. This will suppress all warnings.
import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)
#

parser = argparse.ArgumentParser(description='Extract EC numbers from a genbank file')

parser.add_argument('-g', '--genbank',
    help="Genbank file path",
    required=True)

args = parser.parse_args()

for seq_record in SeqIO.parse(args.genbank, "genbank"):
    for feature in seq_record.features:
        if feature.type == 'CDS':

            # get locus name
            locus = ""
            if 'locus_tag' in feature.qualifiers:
                locus = feature.qualifiers['locus_tag'][0]
            elif 'gene' in feature.qualifiers:
                locus = feature.qualifiers['gene'][0]

            ecList = []

            if 'ec_number' in feature.qualifiers:
                for ec in feature.qualifiers['ec_number']:
                    ecList.append(ec)

            # get functions
            if 'product' in feature.qualifiers:
                for product in feature.qualifiers['product']:
                    ecListProduct = re.findall(r"EC [0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+", product)
                    ecList = ecList + ecListProduct

            if 'function' in feature.qualifiers:
                for function in feature.qualifiers['function']:
                    ecListFunction = re.findall(r"EC [0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+", function)
                    ecList = ecList + ecListFunction

            # Merge and Clean
            ecList = f.cleanEC(ecList)

            # print
            if len(ecList) > 0:
            #print(locus,function,sep="\t",end="\t")
                print(locus,end="\t")
                print(*ecList,sep=";")
