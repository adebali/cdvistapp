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
        with open(self.inputFile, 'r') as filein:
            for line in filein:
                if line.startswith("#"):  # Skip comments
                    continue
                
                ll = line.strip().split('\t')
                if len(ll) < kTopologyColumnNumber:  # Ensure sufficient columns
                    raise ValueError(f"Line does not have enough columns: {line.strip()}")
                
                proteinHeader = ll[0]  
                domainName = ll[1]
                domainStart = int(ll[2])
                domainEnd = int(ll[3])

                domainDictionary[domainName] = domainDictionary.get(domainName, [])
                domainDictionary[domainName].append([domainStart, domainEnd])
        
        for domainName, domains in domainDictionary.items():
            self.name = domainName
            self.domains = domains
            self.checkResultAndPush_()
            self.reset_()

        return self

    def reset_(self):
        self.domains = []
        self.name = ''
        return self


