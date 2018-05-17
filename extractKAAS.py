#! /usr/bin/env python

import re
import os
import argparse
import tools.anno
import sys

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description='Extract EC numbers from a KEGG?KAAS output file')

parser.add_argument('-k', '--kaas',
    help="KEGG/KAAS File",
    required=True)

args = parser.parse_args()

## PROCESS MAP FILE ############################################################

koMap = {}

koFile = os.path.dirname(sys.argv[0]) + "/tools/koOrthology.txt"
for line in open(koFile, 'rt'):
    line = line.rstrip()

    split = line.split("\t")
    ko = split[0].split(":")[1]
    product = split[1]

    koMap[ko] = {'product' : product}

ecFile = os.path.dirname(sys.argv[0]) + "/tools/koEC.txt"
for line in open(ecFile, 'rt'):
    line = line.rstrip()

    split = line.split("\t")
    ko = split[0].split(":")[1]
    ec = split[1].split(":")[1]

    if ko in koMap:
        if 'EC_number' in koMap[ko]:
            koMap[ko]['EC_number'].append(ec)
        else:
            koMap[ko]['EC_number'] = [ec]

    else:
        koMap[ko] = {'EC_number' : [ec]}

## PROCESS KEGG FILE ###########################################################

lines = [line.strip() for line in open(args.kaas)]

for line in lines:
    if not line.lstrip().startswith('#'):
        line = line.rstrip()
        split = line.split('\t')
        if len(split) == 2:
            gene = split[0]
            ko = str(split[1])

            if ko in koMap:
                print(gene, 'product', koMap[ko]['product'], sep = "\t")
                print(gene, 'db_xref', "KO:"+str(ko), sep = "\t")

                if 'EC_number' in koMap[ko]:
                    for ec in koMap[ko]['EC_number']:
                        print(gene, 'EC_number', ec, sep = "\t")
