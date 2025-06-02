#!/usr/bin/python
import os
import re
from utils import jsonFile2dict

# Constants
kNumberOfDomainFields = 17

#  HmmscanResultStream parses the textual output from the HMMER3 hmmscan tool and streams out all the domain hits for each query sequence.

class HmmscanResult():
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.results = []
        self.reset_()
        self.parse_()

    ## ------------------------------------------
    ## Private Methods
    def checkResultAndPush_(self):
        if not self.queryName_:
            raise ValueError('Missing sequence name')

        if not self.queryLength_:
            raise ValueError('Missing sequence length')

        self.results.append({
            'queryName': self.queryName_,
            'queryLength': self.queryLength_,
            'domains': self.domains_
        })

    def parse_(self):
        filein = open(self.inputFile ,'r')
        for line in filein:

            if self.skipRemainingLines_: 
                lineIsRecordSeparator = line[0] == '/' and line[1] == '/'
                if lineIsRecordSeparator:
                    self.sortDomainsByConditionalEvalue_()
                    self.checkResultAndPush_()
                    self.reset_()
            
            if re.match('^Query:.*\[L=.*]', line):
                self.parseHeader_(line)
            elif (line[0] == '>' and line[1] == '>'):
                self.parseDomainName_(line)
            elif re.match('^\s+\d+\s+!', line):
                self.parseDomainHit_(line)
            elif re.match('^Internal pipeline statistics', line):
                self.skipRemainingLines_ = True
        return self

    def isComment_(self, line):
        return line[0] == '#'

    def parseHeader_(self, line):
        matches = re.search('^Query:\s+(\S+)\s+\[L=(\d+)\]', line)
        self.queryName_ = matches.group(1)
        self.queryLength_ = int(matches.group(2))

    def parseDomainName_(self, line):
        matches = re.search('^>>\s+(\S+)', line)
        if (not matches):
            raise ValueError('Error while parsing domain name')

        self.currentDomainName_ = matches.group(1)

    def parseDomainHit_(self, line):
        dMatch = re.split('\s+', line)
        if len(dMatch) - 1 != kNumberOfDomainFields:
            raise ValueError("Expected %d elements of data (line: %s)" % (kNumberOfDomainFields, line))

        self.domains_.append({
            'name': self.currentDomainName_,
            'score': float(dMatch[3]),
            'bias': float(dMatch[4]),
            'c_evalue': float(dMatch[5]),
            'i_evalue': float(dMatch[6]),
            'hmm_from': int(dMatch[7]),
            'hmm_to': int(dMatch[8]),
            'hmm_cov': dMatch[9],
            'ali_from': int(dMatch[10]),
            'ali_to': int(dMatch[11]),
            'ali_cov': dMatch[12],
            'env_from': int(dMatch[13]),
            'env_to': int(dMatch[14]),
            'env_cov': dMatch[15],
            'acc': float(dMatch[16])
            })

    def reset_(self):
        self.queryName_ = None
        self.queryLength_ = None
        self.currentDomainName_ = None
        self.domains_ = []
        self.skipRemainingLines_ = False
        return self

    def sortDomainsByConditionalEvalue_(self):
        self.domains_ = sorted(self.domains_, key=lambda k: k['c_evalue'], reverse=False)

