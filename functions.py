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

def incrementVersion(seq_record):
    if "sequence_version" in seq_record.annotations:
        version = seq_record.annotations["sequence_version"] + 1
        seq_record.id = str(seq_record.name) + "." + str(version)

    else:
        seq_record.id = str(seq_record.name) + "." + str(1)

    return(seq_record)
