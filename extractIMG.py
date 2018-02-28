#! /usr/bin/env python

import re
import os
import argparse
import tools.anno
import sys
from Bio import SeqIO

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = 'Extract features from various IMG output files')

parser.add_argument('-gb', '--genbank',
    help = "Genbank file (EC_number, product)",
    required = False)

parser.add_argument('-gf', '--gff',
    help = "GFF file (product)",
    required = False)

parser.add_argument('-c', '--cog',
    help = "COG file (product, COGs)",
    required = False)

parser.add_argument('-i', '--interpro',
    help = "Interpro file (product, interpro, GO)",
    required = False)

parser.add_argument('-k', '--kegg',
    help = "KEGG file (product, EC_number, KO)",
    required = False)

parser.add_argument('-t', '--tigr',
    help = "TIGRFAM file (product)",
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

if args.gff != None:
    lines = [line.strip() for line in open(args.gff)]

    for line in lines:
        if not line.lstrip().startswith('#'):
            line = line.rstrip()
            split = line.split('\t')
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

## COG FILE ####################################################################

if args.cog != None:
    if args.gff == None:
        print("ERROR: GFF file (-gf) required to map COG IDs to locus_tags")
        sys.exit(2)
    else:
        lines = [line.strip() for line in open(args.cog)]

        for line in lines:
            if not line.lstrip().startswith('gene_oid'):
                line = line.rstrip()
                split = line.split('\t')

                geneID = split[0]
                cog = split[9]
                product = split[10]

                print(id2locus[geneID], 'product', product, sep = "\t")
                print(id2locus[geneID], 'db_xref', "COG:" + cog, sep = "\t")

## INTERPRO FILE ###############################################################

if args.interpro != None:
    if args.gff == None:
        print("ERROR: GFF file (-gf) required to map INTERPRO IDs to locus_tags")
        sys.exit(2)
    else:
        lines = [line.strip() for line in open(args.interpro)]

        for line in lines:
            if not line.lstrip().startswith('gene_oid'):
                line = line.rstrip()
                split = line.split('\t')
                if len(split) > 6:
                    geneID = split[0]
                    ipr = split[6]
                    product = split[7]

                    print(id2locus[geneID], 'product', product, sep = "\t")
                    print(id2locus[geneID], 'db_xref', "interpro:" + ipr, sep = "\t")

                    if len(split) > 8:
                        goList = split[8].split("|")
                        for go in goList:
                            print(id2locus[geneID], 'db_xref', go, sep = "\t")

## KEGG FILE ###################################################################

# copied from extractKAAS.py
koMap = {}

koFile = os.path.dirname(sys.argv[0]) + "/tools/keggNameDefs.txt"
for line in open(koFile, 'rt'):
    line = line.rstrip()

    split = line.split("\t")
    ko = split[0]
    product = split[1]

    koMap[ko] = {'product' : product}

ecFile = os.path.dirname(sys.argv[0]) + "/tools/kegg2EC.txt"
for line in open(ecFile, 'rt'):
    line = line.rstrip()

    split = line.split("\t")
    ko = split[0]
    product = split[2].split(" [")[0]
    ec = tools.anno.cleanEC(split[3:])

    if ko in koMap:
        koMap[ko]['EC_number'] = ec
    else:
        koMap[ko] = {'product' : product,
                     'EC_number' : ec}

if args.kegg != None:
    if args.gff == None:
        print("ERROR: GFF file (-gf) required to map KEGG IDs to locus_tags")
        sys.exit(2)
    else:
        lines = [line.strip() for line in open(args.kegg)]

        for line in lines:
            if not line.lstrip().startswith('gene_oid'):
                line = line.rstrip()
                split = line.split('\t')

                gene = id2locus[split[0]]
                ko = split[9].split(":")[1]

                if ko in koMap:
                    print(gene, 'product', koMap[ko]['product'], sep = "\t")
                    print(gene, 'db_xref', "KO:"+str(ko), sep = "\t")

                    if 'EC_number' in koMap[ko]:
                        for ec in koMap[ko]['EC_number']:
                            print(gene, 'EC_number', ec, sep = "\t")

## TIGR FILE ###################################################################

if args.tigr != None:
    if args.gff == None:
        print("ERROR: GFF file (-gf) required to map TIGR IDs to locus_tags")
        sys.exit(2)
    else:
        lines = [line.strip() for line in open(args.tigr)]

        for line in lines:
            if not line.lstrip().startswith('gene_oid'):
                line = line.rstrip()
                split = line.split('\t')

                geneID = split[0]
                tigr = split[6]
                product = split[7]

                print(id2locus[geneID], 'product', product, sep = "\t")
                print(id2locus[geneID], 'db_xref', "TIGR:" + tigr, sep = "\t")
