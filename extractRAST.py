#! /usr/bin/env python

import re
import os
import argparse
import tools.anno
import sys

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = 'Extract Functions and EC numbers from a RAST tab-delimited output file')

parser.add_argument('-r', '--rast',
    help = "RAST File",
    required = True)

args = parser.parse_args()

## PROCESS RAST FILE ###########################################################
lines = [line.strip() for line in open(args.rast)]

for line in lines:
    if not line.lstrip().startswith('contig_id'):
        line = line.rstrip()
        split = line.split('\t')

        if split[2] == "peg": # if protein encoding gene

            # get locus_tag
            locus_tag = split[8].split(",")[0].split("|")[1]

            # products and ecs
            functionList = re.split(' / |; | @ ', split[7])

            for function in functionList:
                print(locus_tag, "product", function, sep = "\t")

                ecList = re.findall(r"[0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+", function)
                ecList = tools.anno.cleanEC(ecList)
                if len(ecList) > 0:
                    for ec in ecList:
                        print(locus_tag, "EC_number", ec, sep = "\t")

            figfam = split[9]
            if len(figfam) > 0:
                print(locus_tag, "db_xref", 'figfam:'+figfam, sep = "\t")
