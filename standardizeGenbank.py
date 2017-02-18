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

parser.add_argument('-p', '--pseudogenes',
    action = "store_true",
    help="Allow pseudogenes to be included, default=don't")

keeperQualifiers = ['protein_id', 'locus_tag', 'translation']

locusTagFields = ['gene', 'gene_synonym', 'locus_tag', 'old_locus_tag']

args = parser.parse_args()

for seq_record in SeqIO.parse(args.genbank, "genbank"):

    # for IMG
    seq_record.id = seq_record.description

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

            # just for IMG genomes
            feature.qualifiers['protein_id'] = [locusTag]

            # remove all but the "keepers"
            for qualifier in feature.qualifiers:
                if qualifier not in keeperQualifiers:
                    feature.qualifiers[qualifier] = []
                else:
                    feature.qualifiers[qualifier] = feature.qualifiers[qualifier]

            # print all (allow pseudogenes) or only print if all keepers are present
            if args.pseudogenes == False:
                allow = 1
                for qualifier in keeperQualifiers:
                    if qualifier not in feature.qualifiers:
                        allow = 0
                if allow == 1:
                    new_features.append(feature)
            else:
                new_features.append(feature)

    seq_record.features = new_features

    ### Write to file
    output_handle = open(args.genbank+".cleaned_"+timestamp+".gbk", "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
