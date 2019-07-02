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

parser.add_argument('-e', '--ec_number',
                    action="store_true",
                    help="Extract EC numbers from the EC_number field (does not currently get them from products or functions)")

parser.add_argument('-k', '--kegg',
                    action="store_true",
                    help="Extract KEGG IDs from the db_xref 'KO' field")

parser.add_argument('-p', '--product',
                    action="store_true",
                    help="Extract products from the `product` field")

args = parser.parse_args()

## LOOP ########################################################################

for seq_record in SeqIO.parse(args.genbank, "genbank"):
    for feature in seq_record.features:

        # get locus_tag
        locus_tag = ""
        for key in feature.qualifiers:
            if key == "locus_tag":
                locus_tag = feature.qualifiers[key][0]

        for key in feature.qualifiers:

            # EC_NUMBER
            if key == "EC_number" and args.ec_number == True:
                for ec in feature.qualifiers[key]:
                    print(locus_tag, ec, sep="\t")

            # KEGG
            if key == "db_xref" and args.kegg == True:
                for db_xref in feature.qualifiers[key]:

                    split = db_xref.split(":")
                    key = split[0]
                    value = split[1]
                    if key == "KO":
                        print(value)

            # PRODUCT
            if key == "product" and args.product == True:
                print(len(feature.qualifiers[key]))
                # for product in feature.qualifiers[key]:
                #    print(locus_tag, product, sep = "\t")
