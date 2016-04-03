import re
import os
import argparse

parser = argparse.ArgumentParser(description='Extract product, EC_number, ecPath, KEGG, GO and signalP results from a PFP output file')

parser.add_argument('-p', '--pfp',
    help="Path to PFP output",
    required=True)

args = parser.parse_args()

##### CLASSES #####

class pfp:
    pfpList = []
    
    def __init__(self, name, product, ec, ecPath, kegg, go, signalP):
        pfp.pfpList.append(self)
        self.name = name
        self.product = product
        self.ec = list(set(ec))
        self.ecPath = list(set(ecPath))
        self.kegg = list(set(kegg))
        self.go = list(set(go))
        self.signalP = signalP
        

##### READ IN PFP RESULTS #####
pfpRaw = {}
pfpCDSCount = 0

pfpFile = open(args.pfp, 'rt')

while True:
    line = pfpFile.readline()
    line = line.rstrip()
    split = line.split('\t')
    if len(split) > 2:   
        name = split[2]
        nameSplit = name.split('|')
        if len(nameSplit) > 2:
            if nameSplit[-2] in pfpRaw:
                pfpRaw[nameSplit[-2]].append(line)
            else:
                pfpCDSCount += 1
                pfpRaw[nameSplit[-2]] = [line]
    
    if not line:
        break

##### PROCESS PFP INFO AND FIND EXTRACT RELEVANT DATA #####
pfpProcessed = {}        

for protein in pfpRaw:
    product = []
    ec = []
    ecPath = []
    kegg = []
    go = []
    signalP = ['signalP:NO']
    
    for line in pfpRaw[protein]:
        split = line.split("\t")
        
        ## Product
        if len(split) >= 5:
            if split[4] != '':
                product.append(split[4])
                
        ## ECs
        #ecList = re.findall(r"[0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+", line) # Loose
        ecList = re.findall(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", line) # Strict
        ec = ec + ecList
        
        ## EC Pathways
        ecPathList = re.findall(r"ec[0-9]{5}", line)   
        ecPath = ecPath + ecPathList
        
        ## KEGGs
        keggList = re.findall(r"K[0-9]{5}", line)
        kegg = kegg + keggList
        
        ## GO Terms
        goList = re.findall(r"GO\:[0-9]+", line) # GO:0043565
        go = go + goList
        
        if len(split) >= 15:
            if split[14].upper() == "YES":
                signalP = ['signalP:YES']
                
    #chrome,location = proteinLocations[protein].split("\t")
    
    #locus_tag = str(locusTags[protein][0])
    
    pfp(protein,product,ec,ecPath,kegg,go,signalP)
    
for protein in pfp.pfpList:
    
    # print product
    for product in protein.product:
        print(protein.name+"\t"+product+"\tproduct")    

    # print EC_number
    for ec_number in protein.ec:
        print(protein.name+"\t"+ec_number+"\tEC_number")  
        
    # print db_xref qualifiers
    
    ## print ecPath
    for ecPath in protein.ecPath:
        print(protein.name+"\tecPath:"+ecPath+"\tdb_xref")  
        
    ## print kegg
    for kegg in protein.kegg:
        print(protein.name+"\tKEGG:"+kegg+"\tdb_xref")  
        
    ## print go
    for go in protein.go:
        print(protein.name+"\t"+go+"\tdb_xref")  
    
    ## print signalP
    for signalP in protein.signalP:
        print(protein.name+"\t"+signalP+"\tdb_xref")  