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
    
args = parser.parse_args()

#genbankFH = "/Users/kimbrel1/Dropbox/LLNL/Genomes/NCBI/Phaeobacter_gallaeciensis_DSM_26640_uid232357/NC_023137.gbk"
#genbankFH = "/Users/kimbrel1/Dropbox/LLNL/Projects/Microalgae/Phaeobacter/Phaeobacter_26640_RAST_output_Genbank.gbk"
genbankFH = args.genbank

featureTypePrint = ["CDS","rRNA","tRNA"]
qualifierTypePrint = ["locus_tag","db_xref","translation","EC_number","product"]
#dbTypePrint = ["SEED","GO","GI","CDD","GeneID"]


for seq_record in SeqIO.parse(genbankFH, "genbank"):
    
    if args.id == "all" or args.id == str(seq_record.id):
    
        print("ID: "+seq_record.id)
        print("Description: "+seq_record.description)
        
        featureTypeCount = {}
        qualifierCount = {}
        db_xrefCount = {}
        
        uniqueLocusTags = {}
        uniquedb_xref= {}
        uniqueEC = {}
        uniqueProduct = {}
        
        for record in seq_record.features:
            featureTypeCount[record.type] = featureTypeCount.get(record.type, 0) + 1
            
            for key in record.qualifiers:
                qualifierCount[key] = qualifierCount.get(key, 0) + 1
                
                # get unique qualifiers
            
                ## locus_tag
                if key == 'locus_tag':
                    for tag in record.qualifiers[key]:
                        uniqueLocusTags[tag] = 0            
                
                ## EC        
                if key == 'EC_number':
                    for ec in record.qualifiers[key]:
                        uniqueEC[ec] = 0   
                
                ## Product        
                if key == 'product':
                    for product in record.qualifiers[key]:
                        uniqueProduct[product] = 0   
                        
                # get more detail about db_xref
                if key == 'db_xref':
                    for db in record.qualifiers[key]:
                        hit = db.split(":")[0]
                        db_xrefCount[hit] = db_xrefCount.get(hit, 0) + 1
                        uniquedb_xref[db] = 0
        
        print("Feature Types:")
        for featureType in featureTypePrint:
            if featureType in featureTypeCount:
                print("\t"+featureType+": "+str(featureTypeCount[featureType]))
        
        print("Qualifier Types:")
        for qualifier in qualifierTypePrint:
            if qualifier in qualifierCount:
                if qualifier == 'locus_tag':
                    print("\t"+qualifier+": "+str(qualifierCount[qualifier])+" ("+str(len(uniqueLocusTags))+" unique)")
                elif qualifier == 'EC_number':
                    print("\t"+qualifier+": "+str(qualifierCount[qualifier])+" ("+str(len(uniqueEC))+" unique)")
                elif qualifier == 'product':
                    print("\t"+qualifier+": "+str(qualifierCount[qualifier])+" ("+str(len(uniqueProduct))+" unique)")
                else:
                    print("\t"+qualifier+": "+str(qualifierCount[qualifier]))
                
        print("db_xref Types:")
        for db in db_xrefCount:
            
            # get count
            counter = 0
            for hit in uniquedb_xref:
                if hit.startswith(db):
                    counter = counter + 1
            
            print("\t"+db+": "+str(db_xrefCount[db])+" ("+str(counter)+" unique)")
            
        print("##")