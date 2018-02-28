from Bio import SeqIO
import re, sys, os
import argparse
import datetime
import tools.gb
import tools.anno

## MISC ########################################################################

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
toolsPath = os.path.dirname(os.path.abspath(sys.argv[0])) + "/tools"

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description='Add or overwrite annotations in a genbank file')

parser.add_argument('-g', '--genbank',
    help = "Genbank file to update",
    required = True)
parser.add_argument('-o', '--out',
    help = "Output File",
    required = True)
parser.add_argument('-c', '--additionalComment',
    required = False,
    default = None,
    help = "Add to the comment line, default = NO")

args = parser.parse_args()

## CLEAN GENBANK FILE ##########################################################

for seq_record in SeqIO.parse(args.genbank, "genbank"):

    ## for IMG
    seq_record.id = seq_record.description

    ###### Update comments and version #########################################

    seq_record = tools.gb.addComment(seq_record, "=====" + timestamp + "=====")
    seq_record = tools.gb.addComment(seq_record, "program=cleanGenbankProducts.py")
    argsDict = vars(args)
    for arg in argsDict:
        seq_record = tools.gb.addComment(seq_record, (str(arg) + "=" + str(argsDict[arg])))

    #seq_record = tools.gb.incrementVersion(seq_record)

    ###### Update Annotations ##################################################

    for feature in seq_record.features: #iterate through features

        newEC = []
        for key in feature.qualifiers:
            if key == "product":
                print("\n***", feature.qualifiers['locus_tag'][0], "***")
                print("initial", feature.qualifiers['product'], sep = "\t")

                products, newEC = tools.anno.cleanProducts(toolsPath, feature.qualifiers['product'])

                feature.qualifiers['product'] = products
                print("final", feature.qualifiers['product'], sep = "\t")


        # add ECs
        if len(newEC) > 0:
            print("ECs", newEC, sep = "\t")
            if "EC_number" in feature.qualifiers:
                feature.qualifiers['EC_number'] += newEC

                feature.qualifiers['EC_number'] = tools.anno.cleanEC(feature.qualifiers['EC_number'])
            else:
                feature.qualifiers['EC_number'] = newEC


    ###### Write ###############################################################

    output_handle = open(args.out, "a")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
