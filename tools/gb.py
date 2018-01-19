def incrementVersion(seqRecord, inc = True):
    if "sequence_version" in seqRecord.annotations:
        version = seqRecord.annotations["sequence_version"]
        if inc == True:
            version += 1
        seqRecord.id = str(seqRecord.name) + "." + str(version)

    else:
        seqRecord.id = str(seqRecord.name) + "." + str(1)

    return(seqRecord)

def addComment(seqRecord, newComment):

    # is there a comments field?
    if "comment" in seqRecord.annotations:
        comments = seqRecord.annotations["comment"]
    else:
        comments = []

    # check to see if it has already been formatted to a list
    if not isinstance(comments, list):
        comments = comments.split("\n")

    comments.append(newComment)
    seqRecord.annotations["comment"] = comments

    return(seqRecord)
