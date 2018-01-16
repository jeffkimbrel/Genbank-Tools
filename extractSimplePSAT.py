import os
import argparse
import tools.anno

## OPTIONS #####################################################################

parser = argparse.ArgumentParser(description='Extract EC, ECdesc and ecPath from a PSAT output file')

parser.add_argument('-p', '--psat',
    help="PSAT output",
    required=True)

args = parser.parse_args()

## FUNCTIONS ###################################################################

def getGeneName(geneFull):
    junk, gene = geneFull.split("/")
    return(gene)

def getPathways(pathwayFull):
    pathway = []

    if pathwayFull != "No pathway identified":

        split = pathwayFull.split("|")

        for value in split:
            valueSplit = value.split("  ")

            if len(valueSplit) == 2:
                pathway.append(valueSplit[0] + "=" + valueSplit[1])

    return(pathway)

## LOOP ########################################################################

lines = [line.strip() for line in open(args.psat)]

results = {}

for line in lines:
    if not line.lstrip().startswith('#'):
        line = line.rstrip()
        split = line.split('\t')
        if len(split) >= 5:
            geneFull, ec, product, pathwayFull = split[2:6]

############### EXTRACTION #####################################################
            if len(ec) > 0:
                gene = getGeneName(geneFull)
                pathway = getPathways(pathwayFull)

                if gene in results:
                    results[gene]["ec"].append(ec)
                    results[gene]["product"].append(product)
                    results[gene]["pathway"] += pathway
                else:
                    results[gene] = {"ec" : [ec],
                                     "product" : [product],
                                     "pathway" : pathway
                                    }

## PRINT RESULTS ###############################################################
for gene in sorted(results.keys()):

    ## EC
    results[gene]["ec"] = tools.anno.cleanEC(results[gene]["ec"])
    for ec in results[gene]["ec"]:
        print(gene, "EC_number", ec, sep = "\t")

    ## PRODUCT
    for product in results[gene]["product"]:
        print(gene, "product", product, sep = "\t")

    ## PATHWAY

    results[gene]["pathway"] = list(set(results[gene]["pathway"]))

    for pathway in results[gene]["pathway"]:
        pathway = "pathway:" + str(pathway)
        print(gene, "db_xref", pathway, sep = "\t")
