from Bio import SeqIO
import re
import os
import argparse

parser = argparse.ArgumentParser(description='Summarize the contents of a genbank file or record')

parser.add_argument('-g', '--genbank',
    help="Genbank file to summarize",
    required=True)
    
parser.add_argument('-i', '--id',
    default="all",
    help="Limit to only the record with this ID" )

parser.add_argument('-c', '--combine',
    action = "store_true", 
    help="Combine all records into a single summary" )
    
args = parser.parse_args()

features = {}
qualifiers = {}
db_xref = {}

for seq_record in SeqIO.parse(args.genbank, "genbank"):
    if args.id == "all" or args.id == str(seq_record.id):
        
## INCREASE COUNT OF FEATURE TYPE IN features DICTIONARY
        for feature in seq_record.features:
            features[feature.type] = features.get(feature.type, 0) + 1
            
## GET QUALIFIERS OF FEATURES
            for qualifierKey in feature.qualifiers:
                for qualifierValue in feature.qualifiers[qualifierKey]:
                    
                    if qualifierKey in qualifiers: ## IF SO, THEN APPEND QUALIFIER VALUE TO LIST
                        qualifiers[qualifierKey].append(qualifierValue)
                    else: # OTHERWISE, ADD NEW
                        qualifiers[qualifierKey] = [qualifierValue]
                
## GET DB_XREF TYPES    
                    if qualifierKey == 'db_xref':
                        db = qualifierValue.split(":")
                        
                        if db[0] in db_xref: ## IF SO, THEN APPEND QUALIFIER VALUE TO LIST
                            db_xref[db[0]].append(db[1])
                        else: # OTHERWISE, ADD NEW
                            db_xref[db[0]] = [db[1]]
            
## DISPLAY IF -c FLAG IS FALSE
        if args.combine == False:
            print("ID: "+seq_record.id)
            print("Description: "+seq_record.description)
            for featureType in features:    
                print("\t"+featureType+": "+str(features[featureType]))
                
                
            print("Qualifier Types:")
            for qualifierType in qualifiers: 
                unique = str(len(list(set(qualifiers[qualifierType]))))
                print("\t"+qualifierType+": "+str(len(qualifiers[qualifierType]))+" ("+unique+" unique)")
                
            print("db_xref Types:")
            for dbType in db_xref: 
                unique = str(len(list(set(db_xref[dbType]))))
                print("\t"+dbType+": "+str(len(db_xref[dbType]))+" ("+unique+" unique)")
                
## RESET DICTIONARIES
            features = {}
            qualifiers = {}
            db_xref = {}

## DISPLAY IF -c FLAG IS TRUE
if args.combine == True:
    print("All Records")
    print("Feature Types:")
    for featureType in features:    
        print("\t"+featureType+": "+str(features[featureType]))
        
    print("Qualifier Types:")
    for qualifierType in qualifiers: 
        unique = str(len(list(set(qualifiers[qualifierType]))))
        print("\t"+qualifierType+": "+str(len(qualifiers[qualifierType]))+" ("+unique+" unique)")
        
    print("db_xref Types:")
    for dbType in db_xref: 
        unique = str(len(list(set(db_xref[dbType]))))
        print("\t"+dbType+": "+str(len(db_xref[dbType]))+" ("+unique+" unique)")