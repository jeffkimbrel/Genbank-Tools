def incrementVersion(seq_record):
    if "sequence_version" in seq_record.annotations:
        version = seq_record.annotations["sequence_version"] + 1
        seq_record.id = str(seq_record.name) + "." + str(version)

    else:
        seq_record.id = str(seq_record.name) + "." + str(1)

    return(seq_record)

def addComment(seq_record, text):
    comments = seq_record.annotations["comment"].split("\n")
    comments.append(text)
    seq_record.annotations["comment"] = comments

    return(seq_record)
