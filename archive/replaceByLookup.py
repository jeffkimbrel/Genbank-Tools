import re
import os
import argparse

parser = argparse.ArgumentParser(description='Give it a 2 column list of terms, and it will replace the term in the first column with the second term in the specified file')

parser.add_argument('-f', '--file',
    help="File with text to replace",
    required=True)

parser.add_argument('-l', '--lookup',
    help="Lookup table",
    required=True)

parser.add_argument('-r', '--replace',
    default=1,
    help="Column with terms to look for" )

parser.add_argument('-w', '--withThis',
    default=2,
    help="Column with terms to look for" )

args = parser.parse_args()

lookupDict = {}
lookupFile = open(args.lookup, 'rt')

while True:
    line = lookupFile.readline()
    line = line.rstrip()
    split = line.split('\t')
    if len(split) > 1:
        lookupDict[split[int(args.replace) - 1]] = split[int(args.withThis) - 1]

    if not line:
        break

#
original = open(args.file, 'rt')
while True:
    line = original.readline()
    line = line.rstrip()
    for key in lookupDict:
        line = line.replace(lookupDict[key],key)
        #print(key,lookupDict[key])
    print(line)

    if not line:
        break
