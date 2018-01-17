from Bio import SeqIO
import re
import os
import argparse
import datetime
import tools.gb

## MISC #####################################################################

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description='Add or overwrite annotations in a genbank file')

parser.add_argument('-g', '--genbank',
    help = "Genbank file to update",
    required = True)
parser.add_argument('-a', '--annotations',
    help = "File with annotations. Expects three tab-separated columns with 'locus_tag', 'qualifier', 'value'",
    required = True)
parser.add_argument('-o', '--out',
    help = "Output File",
    required = True)
parser.add_argument('-c', '--additionalComment',
    required = False,
    default = None,
    help = "Add to the comment line, default = NO")
    
args = parser.parse_args()

## PROCESS ANNOTATIONS FILE ####################################################
lines = [line.strip() for line in open(args.annotations)]

annotations = {}
uniqueQualifiers = []

for line in lines:
    if not line.lstrip().startswith('#'):
        if len(line.split("\t")) == 3:
            line = line.rstrip()
            locus, qualifier, value = line.split("\t")

            uniqueQualifiers.append(qualifier)


            if locus in annotations:
                if qualifier in annotations[locus]:
                    annotations[locus][qualifier].append(value)
                else:
                    annotations[locus][qualifier] = [value]
            else:
                annotations[locus] = {}
                annotations[locus][qualifier] = [value]

uniqueQualifiers = list(set(uniqueQualifiers))

## ADD TO GENBANK FILE #########################################################
for seq_record in SeqIO.parse(args.genbank, "genbank"):

    ## for IMG
    seq_record.id = seq_record.description

    ###### Update comments and version #########################################
    seq_record = tools.gb.addComment(seq_record, "=====" + timestamp + "=====")
    seq_record = tools.gb.addComment(seq_record, "program=updateGenbankAnnotations.py")
    argsDict = vars(args)
    for arg in argsDict:
        seq_record = tools.gb.addComment(seq_record, (str(arg) + "=" + str(argsDict[arg])))

    seq_record = tools.gb.incrementVersion(seq_record)

    ###### Update Annotations ##################################################

    for feature in seq_record.features: #iterate through features
        if 'locus_tag' in feature.qualifiers: # does it have a locus tag
            for locusGB in feature.qualifiers['locus_tag']: #go through locus list
                if locusGB in annotations: #is it found in the annotations

                    for qualifier in uniqueQualifiers:

                        if qualifier in annotations[locusGB]:
                            if qualifier in feature.qualifiers:
                                feature.qualifiers[qualifier] += annotations[locusGB][qualifier]
                            else:
                                feature.qualifiers[qualifier] = annotations[locusGB][qualifier]



    ###### Write ###############################################################
    output_handle = open(args.out, "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
