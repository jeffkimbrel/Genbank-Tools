from Bio import SeqIO
import re
import os
import argparse
import datetime
import tools.gb
import tools.anno

## MISC #####################################################################

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
includedFeatures = ['CDS', 'rRNA', 'tRNA', 'misc_RNA', 'misc_feature', 'misc_bind']

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description='Merge a secondary genbank file into a master by locus_tag and feature type')

parser.add_argument('-m', '--master',
    help = "Master genbank file",
    required = True)
parser.add_argument('-s', '--secondary',
    help = "Secondary genbank file",
    required = True)
parser.add_argument('-o', '--out',
    help = "Output File",
    required = True)
parser.add_argument('-c', '--additionalComment',
    required = False,
    default = None,
    help = "Add to the comment line, default = NO")

args = parser.parse_args()

## CAPTURE SECONDARY FILE INFORMATION ##########################################

secondaryFeatures = {}

for seq_record in SeqIO.parse(args.secondary, "genbank"):
    for feature in seq_record.features:
        if feature.type in includedFeatures:

            secondaryID = feature.qualifiers['locus_tag'][0] + "_" + feature.type
            secondaryFeatures[secondaryID] = feature

## ADD SECONDARY FEATURES TO MASTER ############################################

for seq_record in SeqIO.parse(args.master, "genbank"):

    ## UPDATE COMMENTS AND VERSION #############################################
    seq_record = tools.gb.addComment(seq_record, "=====" + timestamp + "=====")
    seq_record = tools.gb.addComment(seq_record, "program=mergeGenbank.py")

    for feature in includedFeatures:
        seq_record = tools.gb.addComment(seq_record, "includedFeatures="+feature)

    argsDict = vars(args)
    for arg in argsDict:
        seq_record = tools.gb.addComment(seq_record, (str(arg) + "=" + str(argsDict[arg])))

    seq_record = tools.gb.incrementVersion(seq_record)

    ## DO THE UPDATING #########################################################
    for masterFeature in seq_record.features:
        if masterFeature.type in includedFeatures:
            masterID = masterFeature.qualifiers['locus_tag'][0] + "_" + masterFeature.type

            ## ITERATE THROUGH SECONDARY QUALIFIERS ############################

            if masterID in secondaryFeatures:

                for secondaryQualifier in secondaryFeatures[masterID].qualifiers:
                    if secondaryQualifier in masterFeature.qualifiers:

                        masterFeature.qualifiers[secondaryQualifier] += secondaryFeatures[masterID].qualifiers[secondaryQualifier]

                    else:

                        masterFeature.qualifiers[secondaryQualifier] = secondaryFeatures[masterID].qualifiers[secondaryQualifier]

                    if secondaryQualifier == "translation":
                        newTranslations = []
                        for translation in masterFeature.qualifiers[secondaryQualifier]:
                            translation = translation.replace('*', '')
                            newTranslations.append(translation)
                        masterFeature.qualifiers[secondaryQualifier] = newTranslations
                        
                    masterFeature.qualifiers[secondaryQualifier] = list(set(masterFeature.qualifiers[secondaryQualifier]))

    ###### WRITE ###############################################################
    output_handle = open(args.out, "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
