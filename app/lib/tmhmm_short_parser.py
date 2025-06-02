#!/usr/bin/python
import os
import re
from utils import jsonFile2dict

# Constants
kTopologyColumnNumber= 6

#  HmmscanResultStream parses the textual output from the HMMER3 hmmscan tool and streams out all the domain hits for each query sequence.

class TMHMMresult():
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
        filein = open(self.inputFile ,'r')
        for line in filein:
            
            ll = line.strip().split('\t')
            topologyString = ll[kTopologyColumnNumber - 1].strip().split('Topology=')[1]
            print(topologyString)
            intervals = re.split('[io]', topologyString)
            self.firstCharacter_ = topologyString[0]
            for interval in intervals:
                if interval.strip():
                    intervalList = interval.split('-')
                    self.TMdomains_.append([int(intervalList[0]), int(intervalList[1])])
            self.checkResultAndPush_()
            self.reset_()
        return self

    def reset_(self):
        self.TMdomains_ = []
        self.firstCharacter = ''
        return self


