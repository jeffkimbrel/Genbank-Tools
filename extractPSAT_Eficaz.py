import os
import argparse
import tools.anno

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description='Extract Eficaz EC from a PSAT output file')

parser.add_argument('-p', '--psat',
    help="PSAT output",
    required=True)

args = parser.parse_args()

## FUNCTIONS ###################################################################

def getGeneName(geneFull):
    junk, gene = geneFull.split("/")
    return(gene)

## LOOP ########################################################################

lines = [line.strip() for line in open(args.psat)]

results = {}

for line in lines:
    if not line.lstrip().startswith('#'):
        line = line.rstrip()
        split = line.split('\t')
        if len(split) >= 7:
            if len(split[6]) > 0:
                ec = split[3]
                gene = getGeneName(split[2])

                print(gene, "EC_number", ec, sep = "\t")
