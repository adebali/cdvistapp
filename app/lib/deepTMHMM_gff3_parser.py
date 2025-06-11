import pprint

#!/usr/bin/python

# Constants
kTopologyColumnNumber= 4

#  HmmscanResultStream parses the textual output from the HMMER3 hmmscan tool and streams out all the domain hits for each query sequence.

class deepTMHMM():
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.results = []
        self.reset_()
        self.parse_()

    ## ------------------------------------------
    ## Private Methods
    def checkResultAndPush_(self):
        self.results.append({
            'domains': self.domains,
            'name': self.name,
        })

    def parse_(self):
        domainDictionary = {}
        proteinDictionary = {}
        previous_proteinHeader = None

        with open(self.inputFile, 'r') as filein:
            for line in filein:
                if line.startswith("#"):  # Skip comments and metadata
                    continue
                
                if line.startswith("//"):  # Separator between protein entries
                    if previous_proteinHeader:
                        proteinDictionary[previous_proteinHeader] = domainDictionary
                    domainDictionary = {}  # Reset domain dictionary for the next protein
                    previous_proteinHeader = None
                    continue
                
                ll = line.strip().split('\t')
                if len(ll) < 4:  # Ensure sufficient columns
                    raise ValueError(f"Line does not have enough columns: {line.strip()}")
                
                proteinHeader = ll[0]
                domainName = ll[1]
                domainStart = int(ll[2])
                domainEnd = int(ll[3])

                # Initialize domain dictionary for the current domain name
                domainDictionary[domainName] = domainDictionary.get(domainName, [])
                domainDictionary[domainName].append([domainStart, domainEnd])

                # Handle new protein header
                if previous_proteinHeader and proteinHeader != previous_proteinHeader:
                    proteinDictionary[previous_proteinHeader] = domainDictionary
                    domainDictionary = {}  # Reset domain dictionary for the new protein
                    previous_proteinHeader = proteinHeader
                else:
                    previous_proteinHeader = proteinHeader

            # Add the last protein entry to the dictionary
            if previous_proteinHeader:
                proteinDictionary[previous_proteinHeader] = domainDictionary

        # Convert protein dictionary to the desired format
        parsedResults = []
        for proteinName, domainDictionary in proteinDictionary.items():
            domainList = []
            for domainName, domains in domainDictionary.items():
                domainList.append({"name": domainName, "domains": domains})
            parsedResults.append({"protein": proteinName, "domains": domainList})

        self.results = parsedResults

    def reset_(self):
        self.domains = []
        self.name = ''
        return self

# a = deepTMHMM('TMRs.gff3')
# pprint.pprint(a.results)
