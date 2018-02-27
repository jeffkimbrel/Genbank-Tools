import re

def cleanEC(ecList):

    completeList = []
    incompleteList = []

    for ec in ecList:

        # Remove "EC " (rast) and "EC:"
        ec = ec.replace("EC:","")
        ec = ec.replace("EC","")
        ec = ec.replace(" ","")

        if '-' in ec:
            incompleteList.append(ec)
        else:
            completeList.append(ec)

    completeList = list(set(completeList))
    incompleteList = list(set(incompleteList))

    for incompleteEC in list(incompleteList): # iterate through a copy

        for completeEC in completeList:

            if completeEC.startswith(incompleteEC.split('-')[0]):
                if incompleteEC in incompleteList:
                    incompleteList.remove(incompleteEC)

    ecListFinal = incompleteList + completeList

    return(ecListFinal)

def cleanProducts(toolsPath, products):

    productsCopy = products

    ## REMOVE BANNED PRODUCTS ##################################################
    lines = [line.strip() for line in open(toolsPath + "/bannedProducts.txt")]
    bannedProducts = {}
    for line in lines:
        matchType, string = line.split("\t")
        bannedProducts[string.lower()] = matchType.lower()
    for banned in bannedProducts:
        for product in productsCopy:
            if banned.lower() in product.lower():
                products.remove(product)
    productsCopy = products

    ## EXTRACT EC ##############################################################
    productsMinusEC = []
    ecFinalList = []
    for product in productsCopy:
        ecList = re.findall(r" \(*EC [0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+\)*", product)

        # --> can add more types of EC strings here and append to ecList

        # remove from product
        if len(ecList) > 0:
            for ec in sorted(ecList, key=len, reverse=True):
                product = product.replace(ec, "")
                productsMinusEC.append(product)

                # extract and save EC
                smallECList = re.findall(r"[0-9]+\.[0-9\-]+\.[0-9\-]+\.[0-9\-]+", ec)
                for smallEC in smallECList:
                    ecFinalList.append(smallEC)
        else:
            productsMinusEC.append(product)

    products = productsMinusEC

    ## REMOVE DUPLICATES #######################################################
    nonDupeProducts = []

    for product in sorted(products, key=len, reverse=True):
        dupe = 0
        for potential in nonDupeProducts:
            if potential.lower() == product.lower():
                dupe = 1
            elif product.lower() in potential.lower():
                dupe = 1
            elif product.lower().replace(",", "") in potential.lower().replace(",", ""):
                dupe = 1
            elif product.lower().replace("-", "") in potential.lower().replace("-", ""):
                dupe = 1
        if dupe == 0:
            nonDupeProducts.append(product)

    products = nonDupeProducts

    ## RETURN ##################################################################

    return(products, ecFinalList)
