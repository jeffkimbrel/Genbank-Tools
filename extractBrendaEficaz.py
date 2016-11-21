import re
import os
import argparse

parser = argparse.ArgumentParser(description='Extract Brenda and EFICAz EC numbers from PSAT Output')

parser.add_argument('-p', '--psat',
    help="Path to psat output",
    required=True)

args = parser.parse_args()

psatFile = open(args.psat, 'rt')

ecDict = {}

while True:
    line = psatFile.readline()
    line = line.rstrip()

    if not line.lstrip().startswith('#'):
        split = line.split('\t')
        if len(split) > 2:
            nameSplit = split[2].split('/')
            locus_tag = nameSplit[1]

            if split[3] != "":
                ec = split[3]

                if len(split) > 6 and split[6] != "":
                    print(locus_tag,"EFICAz",ec,sep="\t")

                if len(split) > 7 and split[7] != "":
                    print(locus_tag,"BRENDA",ec,sep="\t")



    if not line:
        break
