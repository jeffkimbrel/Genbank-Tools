#! /usr/bin/env python

import re
import os
import argparse
import tools.anno
import sys

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = 'Extract Functions and EC numbers from a RAST tab-delimited output file')

parser.add_argument('-g', '--gff',
    help = "RAST GFF File",
    required = True)

parser.add_argument('-s', '--subsystem',
    help = "RAST Subsystem File",
    default = None,
    required = False)

args = parser.parse_args()

## PROCESS GFF FILE ############################################################

locusMapping = {}

lines = [line.strip() for line in open(args.gff)]

for line in lines:
    if not line.lstrip().startswith('contig_id'):
        line = line.rstrip()
        split = line.split('\t')

        if split[2] == "peg": # if protein encoding gene

            # get locus_tag and add to mapping file
            locus_tag = split[8].split(",")[0].split("|")[1]
            locusMapping[split[1]] = locus_tag

            # products and ecs
            functionList = re.split(' / |; | @ ', split[7])

            for function in functionList:
                print(locus_tag, "product", function, sep = "\t")

                ecList = re.findall(r"[0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+", function)
                ecList = tools.anno.cleanEC(ecList)
                print(ecList)
                if len(ecList) > 0:
                    for ec in ecList:
                        print(locus_tag, "EC_number", ec, sep = "\t")

            figfam = split[9]
            if len(figfam) > 0:
                print(locus_tag, "db_xref", 'figfam:'+figfam, sep = "\t")

## PROCESS SUBSYSTEM FILE ######################################################

if args.subsystem != None:
    lines = [line.strip() for line in open(args.subsystem)]

    for line in lines:
        if not line.lstrip().startswith('contig_id'):
            if not line.startswith('Category'):
                split = line.split('\t')

                subsystem = 'subsystem:' + split[0] + ";" + split[1] + ";" + split[2]

                figSplit = split[4].split(', ')
                for fig in figSplit:
                    print(locusMapping[fig], 'db_xref', subsystem, sep = "\t")
