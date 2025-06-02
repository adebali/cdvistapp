#!/usr/bin/python

class deepTMHMMresult():
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.results = []
        self.reset_()
        self.parse_()

    ## ------------------------------------------
    ## Private Methods
    def checkResultAndPush_(self):
        self.results.append({
            'domains': self.TMdomains_,
            'firstCharacter': self.firstCharacter_,
        })

    def parse_(self):
        firstLine = False
        filein = open(self.inputFile ,'r')
        domainList = []
        for line in filein:
            if line.startswith('>'):
                header = line.strip().split('>')[1]
                firstLine = True
                continue
            if firstLine:
                firstLine = False
                continue
            labels = line.strip()

            intervals = {}
            current_domain = labels[0]
            start = 1  # 1-based coordinate system

            for i in range(1, len(labels)):
                if labels[i] != current_domain:
                    # Close current interval
                    if current_domain not in intervals:
                        intervals[current_domain] = []
                    intervals[current_domain].append([start, i])
                    # Start new interval
                    current_domain = labels[i]
                    start = i + 1  # shift to 1-based coordinate system 
            intervals[current_domain].append([start, i-1])

            for key in intervals:
                domainList.append({
                    'firstCharacter': key,
                    'domains': intervals[key]
                })
            
            self.checkResultAndPush_()
            self.reset_()
        return self

    def reset_(self):
        self.TMdomains_ = []
        self.firstCharacter = ''
        return self


