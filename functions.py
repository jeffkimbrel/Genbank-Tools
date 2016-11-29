def cleanEC(ecList):

    completeList = []
    incompleteList = []

    for ec in ecList:
        if '-' in ec:
            incompleteList.append(ec)
        else:
            completeList.append(ec)

    completeList = list(set(completeList))
    incompleteList = list(set(incompleteList))

    for incompleteEC in list(incompleteList): # iterate through a copy
        for completeEC in completeList:
            if completeEC.startswith(incompleteEC.rstrip('.-')):

                #print(completeEC,incompleteEC,sep="\t")
                if incompleteEC in incompleteList:
                    incompleteList.remove(incompleteEC)

    ecListFinal = incompleteList + completeList

    return(ecListFinal)
