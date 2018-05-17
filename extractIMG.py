#! /usr/bin/env python

import re
import os
import argparse
import tools.anno
import sys
from Bio import SeqIO

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = 'Extract features from IMG GFF or GBK files')

parser.add_argument('-gb', '--genbank',
    help = "Genbank file (EC_number, product)",
    required = False)

parser.add_argument('-gf', '--gff',
    help = "GFF file (product, oldID)",
    required = False)

args = parser.parse_args()

## GENBANK FILE ################################################################

if args.genbank != None:
    for seq_record in SeqIO.parse(args.genbank, "genbank"):
        for feature in seq_record.features:
            ecList = []
            if 'product' in feature.qualifiers:
                for product in feature.qualifiers['product']:
                    print(feature.qualifiers['locus_tag'][0], 'product', product, sep = "\t")
                    ecList = ecList + re.findall(r" \(*EC [0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+\)*", product)
            if 'function' in feature.qualifiers:
                for function in feature.qualifiers['function']:
                    print(feature.qualifiers['locus_tag'][0], 'product', function, sep = "\t")
                    ecList = ecList + re.findall(r" \(*EC [0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+\)*", function)
            if 'EC_number' in feature.qualifiers:
                ecList += feature.qualifiers['EC_number']

            if len(ecList) > 0:
                for ec in ecList:
                    smallList = re.findall(r"[0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+", ec)
                    for smallEC in smallList:
                        print(feature.qualifiers['locus_tag'][0], 'EC_number', smallEC, sep = "\t")

## GFF FILE ####################################################################

id2locus = {}

featureTypes = ['CDS', 'RNA', 'rRNA', 'tRNA']

if args.gff != None:
    lines = [line.strip() for line in open(args.gff)]

    for line in lines:
        if not line.lstrip().startswith('#'):
            line = line.rstrip()
            split = line.split('\t')

            if split[2] in featureTypes:

                features = split[8]
                product = ""
                locus_tag = ""
                geneID = ""

                for sub in features.split(";"):

                    if sub.startswith("product="):
                        product = sub.replace("product=", "").lstrip().rstrip()
                    elif sub.startswith("locus_tag="):
                        locus_tag = sub.replace("locus_tag=", "").lstrip().rstrip()
                    elif sub.startswith("ID="):
                        geneID = sub.replace("ID=", "").lstrip().rstrip()

                id2locus[geneID] = locus_tag

                print(locus_tag, 'product', product, sep = "\t")
                print(locus_tag, 'oldID', geneID, sep = "\t")
