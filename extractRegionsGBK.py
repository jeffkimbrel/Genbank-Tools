#! /usr/bin/env python

from Bio import SeqIO
import os
import argparse
import tools.gb

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description = 'xxx', formatter_class = argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-g', '--genbank',
    help="Genbank file",
    required=True)

parser.add_argument('-c', '--contig',
    help="Contig/Chromosome Name",
    required = True)

parser.add_argument('-b', '--begin',
    help="Beginning Coordinates",
    type=int,
    required = True)

parser.add_argument('-e', '--end',
    help="End Coordinates",
    type=int,
    required = True)

parser.add_argument('-z', '--zero',
    help="Rescale to zero?",
    action = 'store_true')

parser.add_argument('-r', '--reverse',
    help="Reverse strand?",
    action = 'store_true')

args = parser.parse_args()

unit = args.genbank + "_" + args.contig + "_" + str(args.begin) + "-" + str(args.end)

## FUNCTIONS ###################################################################

def findLowest():
    lowest = 99999999999999999
    for feature in features:
        if features[feature].start < lowest:
            lowest = features[feature].start
        if features[feature].stop < lowest:
            lowest = features[feature].stop

    return(lowest-1)

def findHighest():
    highest = 0
    for feature in features:
        if features[feature].start > highest:
            highest = features[feature].start
        if features[feature].stop > highest:
            highest = features[feature].stop

    return(highest)

## CLASSES #####################################################################

class Feature:

    def __init__(self, file, contig, locus_tag, start, stop, strand, type, product):
        self.file = file
        self.contig = contig
        self.locus_tag = locus_tag
        self.start = start
        self.stop = stop
        self.strand = strand
        self.type = type
        self.product = product

    def rescale(self, l):
        self.start = self.start - l
        self.stop = self.stop - l

    def reverse(self, h):
        self.start = h - self.start
        self.stop = h - self.stop

        if self.strand == 'forward':
            self.strand = 'reverse'
        elif self.strand == 'reverse':
            self.strand = 'forward'

    def display(self):
        print(unit, self.file, self.contig, self.locus_tag, self.start, self.stop, self.strand, self.type, self.product, sep = "\t")


## LOOP ########################################################################

features = {}
id = 0

for seq_record in SeqIO.parse(args.genbank, "genbank"):

    if seq_record.id == args.contig:

        for feature in seq_record.features:

            start, stop, strand = tools.gb.parseLocation(feature.location)
            type = feature.type

            if strand == '+':
                strand = "forward"
            elif strand == "-":
                strand = "reverse"

            if start <= args.end:
                if start >= args.begin:

                    # get locus_tag
                    locus_tag = ""
                    for key in feature.qualifiers:
                        if key == "locus_tag":
                            locus_tag = feature.qualifiers[key][0]

                    product = ""

                    for key in feature.qualifiers:

                        ## PRODUCT
                        if key == "product":
                            product = feature.qualifiers[key][0]

                    features[id] = Feature(args.genbank, args.contig, locus_tag, start, stop, strand, type, product)
                    id += 1

lowestValue = findLowest()
highestValue = findHighest()

## PRINT #######################################################################

print("UNIT", "FILE", "CONTIG", "LOCUS_TAG", "START", "STOP", "STRAND", "TYPE", "PRODUCT", sep = "\t")

for feature in features:

    if args.reverse == True:
        features[feature].reverse(highestValue)

    if args.zero == True:
        features[feature].rescale(lowestValue)

    features[feature].display()
