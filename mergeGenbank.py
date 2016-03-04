from Bio import SeqIO
import re
import os

masterGenbankFH = "/Users/kimbrel1/Dropbox/LLNL/Genomes/NCBI/Phaeobacter_gallaeciensis_DSM_26640_uid232357/merged.gbk"
secondaryGenbankFH = "/Users/kimbrel1/Dropbox/LLNL/Projects/Microalgae/Phaeobacter/Phaeobacter_26640_RAST_output_Genbank.gbk"

outputFolder = "/Users/kimbrel1/Dropbox/LLNL/Projects/Microalgae/Phaeobacter/results/output/"

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)
    

##### MAKE MAPPING DICTIONARY FROM ORIGINAL GENBANK FILE #####
proteinLocations = {}
locusTags = {}
mappingCDSCount = 0

for seq_record in SeqIO.parse(masterGenbankFH, "genbank"):
    for record in seq_record.features:
        if record.type == 'CDS':
            mappingCDSCount += 1
            if record.qualifiers['protein_id'][1] not in proteinLocations:
                proteinLocations[record.qualifiers['protein_id'][1]] = seq_record.name+"\t"+str(record.location)
                
                # save locus_tag/protein_id mapping
                locusTags[record.qualifiers['protein_id'][1]] = record.qualifiers['locus_tag']
            else:
                print("ERROR - "+str(record.location)+ "exists twice in the genbank file!!!")
                
        
##### READ IN RAST GENBANK FILE AND DECORATE #####
RASTCDSCount = 0
mappingRASTMATCH = 0

for seq_record in SeqIO.parse(secondaryGenbankFH, "genbank"):
    for record in seq_record.features:
        if record.type == 'CDS':
            RASTCDSCount += 1
            locationSplit = re.split(r'[\(\)\[\]\:]',str(record.location))
            start = locationSplit[1]
            stop = locationSplit[2]
            strand = locationSplit[4]
            
            for protein in pfp.pfpList:
                #print(protein.location,record.location)
                if protein.start == start and protein.stop == stop and protein.strand == strand: #add chromosome compare too for later!
                    mappingRASTMATCH += 1    
                    
                    ## Add protein id
                    record.qualifiers['protein_id'] = protein.name
                    
                    ## Add locus_tag
                    record.qualifiers['locus_tag'] = protein.locus_tag
                    
                    ## Add product
                    newProduct = protein.product
                    if 'product' in record.qualifiers:                    
                        newProduct = newProduct + record.qualifiers['product']
                    
                    newProduct = list(set(newProduct))
                    if newProduct != []:
                        record.qualifiers['product'] = newProduct    
                        
                    ## Add ec numbers
                    newEC = protein.ec
                    if 'EC_number' in record.qualifiers:
                        newEC = newEC + record.qualifiers['EC_number']
                    newEC = list(set(newEC))
                    
                    if ecList != []:
                        record.qualifiers['EC_number'] = newEC
                        
                    ## build db_xref objects (KEGG,GO,signalP,ecPath)
                    
                    dbxref = []
                    
                    # add existing db_xref
                    if 'db_xref' in record.qualifiers:
                        dbxref = dbxref + record.qualifiers['db_xref']
                    
                    # Add ecPath
                    ecPath = protein.ecPath
                    if ecPath != []:
                        for entry in ecPath:
                            dbxref.append("ecPath:"+entry)
                    
                    # Add GO terms
                    goTerms = protein.go
                    if goTerms != []:
                        for entry in goTerms:
                            dbxref.append(entry) 
                    
                    # Add KEGG terms
                    keggTerms = protein.kegg
                    if keggTerms != []:
                        for entry in keggTerms:
                            dbxref.append("KEGG:"+entry) 
                    
                    # Add signalP
                    signalP = protein.signalP
                    if signalP != []:
                        for entry in signalP:
                            dbxref.append(entry) 
                    dbxref = list(set(dbxref))       
                    
                    if dbxref != []:
                        record.qualifiers['db_xref'] = dbxref    
                         
    ### Write to file
    output_handle = open(outputFolder+"/"+seq_record.name+"edit.gbk", "w")
    SeqIO.write(seq_record, output_handle, "genbank")
    output_handle.close()

print("Number of CDS sequences in the mapping file: "+str(mappingCDSCount))
print("Number of CDS sequences in the RAST file: "+str(RASTCDSCount))
print("Number of proteins in the PFP file: "+str(pfpCDSCount))
print("Number of PFP proteins with a RAST gene match: "+str(mappingRASTMATCH))