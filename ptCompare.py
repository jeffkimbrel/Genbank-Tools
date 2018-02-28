import sys

results = {}
files = []

counter = 1
while counter < len(sys.argv):

    file = [line.strip() for line in open(sys.argv[counter])]
    files.append(sys.argv[counter])
    for line in file:
        if not line.lstrip().startswith('#'):
            if not line.startswith('Pathway Name '):
                split = line.rstrip().split("|")
                if len(split) > 1:
                    pathway = split[0]
                    value = split[4]
                    fileName = sys.argv[counter]

                    if pathway in results:
                        results[pathway][fileName] = value
                        results[pathway]['family'] = split[2]

                    else:
                        results[pathway] = {fileName : value, 'family' : split[2]}

    counter += 1

## PRINT
print("PATHWAY\tFAMILY", end = "\t")
for fileName in files:
    print(fileName, end = "\t")
print()

for pathway in sorted(results.keys()):
    print(pathway, end = "\t")
    print(results[pathway]['family'], end = "\t")
    for fileName in files:
        if fileName in results[pathway]:
            print(results[pathway][fileName], end = "\t")
        else:
            print(0, end = "\t")
    print()
