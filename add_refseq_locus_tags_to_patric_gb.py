import argparse
from Bio import SeqIO
import pandas as pd
import tools.gb
import datetime

# RAST/patric output by default has an incorrect header which leads to a BioPython warning. This will suppress all warnings.
import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)

# OPTIONS #####################################################################

parser = argparse.ArgumentParser(
    description='XXX',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-g', '--genbank',
                    required=True)

parser.add_argument('-t', '--txt',
                    required=True)

parser.add_argument('-o', '--out',
                    required=True)

args = parser.parse_args()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# FUNCTIONS ###################################################################


def make_mapping():
    # returns dictionary with fig as key, and locus_tag/fig as value
    df = pd.read_csv(args.txt, sep='\t')
    map = pd.Series(df.aliases.values, index=df.feature_id).to_dict()

    for m in map:
        if str(map[m]).startswith('locus_tag'):
            map[m] = map[m].split(":")[1]
        else:
            map[m] = m
    return(map)


def main():
    map = make_mapping()

    for seq_record in SeqIO.parse(args.genbank, "genbank"):

        # fix incorrect molecule type
        seq_record.annotations['molecule_type'] = tools.gb.fixMoleculeType(
            seq_record.annotations['molecule_type'])

        # add comment
        seq_record = tools.gb.addComment(seq_record, "=====" + timestamp + "=====")
        seq_record = tools.gb.addComment(
            seq_record, "program=add_refseq_locus_tags_to_patric_gb.py")
        argsDict = vars(args)
        for arg in argsDict:
            seq_record = tools.gb.addComment(seq_record, (str(arg) + "=" + str(argsDict[arg])))
        seq_record = tools.gb.incrementVersion(seq_record, inc=False)

        for feature in seq_record.features:
            if 'db_xref' in feature.qualifiers:
                if feature.qualifiers['db_xref'][0].startswith("RAST2"):
                    id = feature.qualifiers['db_xref'][0].split(":")[1]
                    feature.qualifiers['locus_tag'] = map[id]

        ## WRITE ###################################################################

        output_handle = open(args.out, "a")
        SeqIO.write(seq_record, output_handle, "genbank")
        output_handle.close()


main()
