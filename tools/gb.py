def incrementVersion(seqRecord):
    if "sequence_version" in seqRecord.annotations:
        version = seqRecord.annotations["sequence_version"] + 1
        seqRecord.id = str(seqRecord.name) + "." + str(version)

    else:
        seqRecord.id = str(seqRecord.name) + "." + str(1)

    return(seqRecord)

def addComment(seqRecord, newComment):
    comments = seqRecord.annotations["comment"].split("\n")
    comments.append(newComment)
    seqRecord.annotations["comment"] = comments

    return(seqRecord)
