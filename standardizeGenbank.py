from Bio import SeqIO
import re
import os
import argparse
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

## OPTIONS

parser = argparse.ArgumentParser(description='Clean a genbank file')

parser.add_argument('-g', '--genbank',
    help="Genbank file to update",
    required=True)

parser.add_argument('-l', '--locus',
    help="locus tag prefix",
    required=True)

keeperQualifiers = ['protein_id','locus_tag','translation']

locusTagFields = ['gene','gene_synonym']

args = parser.parse_args()


for seq_record in SeqIO.parse(args.genbank, "genbank"):
    new_features = []
    for feature in seq_record.features:
        if feature.type == 'CDS':

            # search for locus tag
            locusTag = ""
            for qualifier in feature.qualifiers:
                if qualifier in locusTagFields:
                    #print(args.locus)
                    for potential in feature.qualifiers[qualifier]:
                        if str(args.locus) in potential:
                            locusTag = potential
            feature.qualifiers['locus_tag'] = [locusTag]

            # remove all but the "keepers"
            for qualifier in feature.qualifiers:
                if qualifier not in keeperQualifiers:
                    feature.qualifiers[qualifier] = []
                else:
                    feature.qualifiers[qualifier] = feature.qualifiers[qualifier]
            new_features.append(feature)

    seq_record.features = new_features

    ### Write to file
    output_handle = open(args.genbank+".cleaned.gbk", "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
