def cleanEC(ecList):

    completeList = []
    incompleteList = []

    for ec in ecList:

        # Remove "EC " (rast) and "EC:"
        ec = ec.replace("EC ","")
        ec = ec.replace("EC:","")

        if '-' in ec:
            incompleteList.append(ec)
        else:
            completeList.append(ec)

    completeList = list(set(completeList))
    incompleteList = list(set(incompleteList))

    for incompleteEC in list(incompleteList): # iterate through a copy
        for completeEC in completeList:
            if completeEC.startswith(incompleteEC.rstrip('-')):

                if incompleteEC in incompleteList:
                    incompleteList.remove(incompleteEC)

    ecListFinal = incompleteList + completeList

    return(ecListFinal)
