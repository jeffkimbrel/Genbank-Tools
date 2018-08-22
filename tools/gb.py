import re

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

def parseLocation(location):

    split = re.split('\[|:|\]|\(|\)', str(location))
    strand = split[4]
    start = ""
    end = ""

    split[1] = split[1].replace("<", "")
    split[2] = split[2].replace("<", "")
    split[1] = split[1].replace(">", "")
    split[2] = split[2].replace(">", "")

    if strand == '-':
        start = split[2]
        end = str(int(split[1]) + 1)
    else:
        start = str(int(split[1]) + 1)
        end = split[2]

    return(int(start), int(end), strand)

def fixMoleculeType(type):
    return(type.upper())
