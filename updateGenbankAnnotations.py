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

# GRAB NEW ANNOTATIONS AND SAVE TO LIST
annotationsFile = open(annotationsFH, 'rt')

annotationsList = []
while True:
    line = annotationsFile.readline()
    line = line.rstrip()
    annotationsList.append(line)
            
    if not line:
        break   

print(str(len(annotationsList))+" annotations in file") 

# ITERATE THROUGH THE GENBANK FILE AND ADD ANNOTATIONS
     
noIdentifier = 0  
        
for seq_record in SeqIO.parse(genbankFH, "genbank"):
    for feature in seq_record.features:
        if feature.type == 'CDS':
            
            # Does the CDS have this type of identifier?
            if identifier in feature.qualifiers:

                for line in list(annotationsList): # iterating over a copy of the list, so I can delete from the real list
                    split = line.split('\t') 
    
                    if (len(split) > 1):
                        
                        lineIdentifier = split[0]
                        lineAnnotation = split[1]
                        
                        # if "col3" special flag has been called. This ignores the -q flag.
                        if qualifier == "col3":
                            lineQualifier = split[2]
                  
                        else: # qualifier comes from the -q flag instead
                            lineQualifier = qualifier
                            
                        
                        # some genbank files may have multiple identifiers... check lineIdentifier against them all
                        for featureIdentifier in feature.qualifiers[args.identifier]:
                            if featureIdentifier == lineIdentifier:
                                
                                ## OK, we have a hit, go ahead and update the record!
                                
                                if len(annotationsList) % 1000 == 0:
                                    print(str(len(annotationsList))+" annotations remaining")
                                
                                if db_xref_type != "none":
                                    lineAnnotation = db_xref_type+":"+lineAnnotation
                                    
                                    
                                if method == "o":
                                    feature.qualifiers[lineQualifier] = lineAnnotation
                                else:
                                    if lineQualifier in feature.qualifiers:
                                        feature.qualifiers[lineQualifier].append(lineAnnotation)
                                    else:
                                        feature.qualifiers[lineQualifier] = [lineAnnotation]
                                annotationsList.remove(line)
                        
                            
                        
                            
            
            
            
            
                
                
                
                            
                            
                            
            else:
                noIdentifier += 1
                
    ### Write to file
    output_handle = open(outputFolder+"/"+seq_record.name+"_updated.gbk", "w")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()
    
print("CDS without "+args.identifier+" identifier: "+str(noIdentifier))
