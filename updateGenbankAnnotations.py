from Bio import SeqIO
import re
import os
import argparse
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# col1=identifier, col2=new annotation
# 

## OPTIONS

parser = argparse.ArgumentParser(description='Add or overwrite annotations in a genbank file')

parser.add_argument('-g', '--genbank',
    help="Genbank file to update",
    required=True)
    
parser.add_argument('-a', '--annotations',
    help="File with annotations (col1=identifier, col2=new annotation)",
    required=True)
    
parser.add_argument('-m', '--method',
    help="'o'=overwite, 'a'=append/add",
    default="a")    

parser.add_argument('-i', '--identifier',
    help="Type of annotation from column 1 of annotations file (ex. 'locus_tag', 'GI') to look for in the genbank file",
    default="locus_tag")

parser.add_argument('-q', '--qualifier',
    help="Qualifier to add new annotations to (ex. 'product', 'db_xref')",
    default="product")
    
parser.add_argument('-x', '--db_xref_type',
    help="If using -q db_xref this option will prepend annotations with this variable, if your annotations file is missing it (ex. 'GO', 'SEED')",
    default="none")
    
parser.add_argument('-f', '--folder',
    help="Output folder, defaults to updatedOutput + timestamp",
    default="updatedOutput_"+timestamp)    

args = parser.parse_args()

genbankFH = args.genbank
annotationsFH = args.annotations
identifier = args.identifier
qualifier = args.qualifier
db_xref_type = args.db_xref_type
outputFolder = args.folder
method = args.method

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder) 

## GRAB NEW ANNOTATIONS
    
annotationsFile = open(annotationsFH, 'rt')
annotations = {}

while True:
    line = annotationsFile.readline()
    line = line.rstrip()
    split = line.split('\t') 
   
    if (len(split) > 1):
        if db_xref_type != "none":
            annotations[split[0]] = db_xref_type+":"+split[1]
        else:
            annotations[split[0]] = split[1]
            
    if not line:
        break   


noIdentifier = 0  
        
## UPDATE GENBANK FILE
for seq_record in SeqIO.parse(genbankFH, "genbank"):
    for feature in seq_record.features:
        if feature.type == 'CDS':
            
            # Does the CDS have this type of identifier?
            if args.identifier in feature.qualifiers:
                
                ## Are any of these qualifiers in the new annotations file?
                for qualifierRecord in feature.qualifiers[args.identifier]:
                    if qualifierRecord in annotations:
                        
                        if method == "o":
                            feature.qualifiers[args.qualifier] = annotations[qualifierRecord]
                        else:
                            feature.qualifiers[args.qualifier].append(annotations[qualifierRecord])
                            
                            
            else:
                noIdentifier += 1
                
    ### Write to file
    output_handle = open(outputFolder+"/"+seq_record.name+"_updated.gbk", "w")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
    
print("CDS without "+args.identifier+"identifier: "+str(noIdentifier))
