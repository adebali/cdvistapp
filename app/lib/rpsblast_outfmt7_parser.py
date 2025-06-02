#!/usr/bin/python
import os
import re
from utils import jsonFile2dict

# Constants
kNumberOfDomainFields = 17

#  HmmscanResultStream parses the textual output from the HMMER3 hmmscan tool and streams out all the domain hits for each query sequence.

class RpsblastResult():
    def __init__(self, inputFile, bitScoreFile):
        self.inputFile = inputFile
        bitScoreStream= open(bitScoreFile, 'r')
        self.bitScores = {}
        for line in bitScoreStream:
            ll = line.split('\t')
            self.bitScores[ll[0]] = {'name': ll[1], 'cutoff': float(ll[2])}

    def getDomains_(self):
        fields = ['query acc.ver', 'subject acc.ver', 'identity', 'alignment length', 'mismatches', 'gap opens', 'q. start', 'q. end', 's. start', 's. end', 'evalue', 'bit score']
        domains = []
        for line in open(self.inputFile, 'r'):
            if not self.isComment_(line) and line.strip():
                ll = line.split('\t')
                domains.append({
                    fields[0] : ll[0],
                    fields[1] : ll[1],
                    fields[2] : float(ll[2]),
                    fields[3] : float(ll[3]),
                    fields[4] : float(ll[4]),
                    fields[5] : float(ll[5]),
                    fields[6] : float(ll[6]),
                    fields[7] : float(ll[7]),
                    fields[8] : float(ll[8]),
                    fields[9] : float(ll[9]),
                    fields[10] : float(ll[10]),
                    fields[11] : float(ll[11])
                })
        return domains

    def acceptDomainAndGetName_(self, domain):
        bitScoreInfo = self.bitScores.get(domain['subject acc.ver'].split(':')[1], False)
        if bitScoreInfo == False:
            return False
        # print(str(bitScoreInfo['cutoff']) + '\t' + str(domain['bit score']))
        if bitScoreInfo['cutoff'] < domain['bit score']:
            domain['subject acc.ver'] = bitScoreInfo['name']
            return domain
        return False

    def getResults(self):
        acceptedDomains = []
        domains = self.getDomains_()
        for domain in domains:
            newDomain = self.acceptDomainAndGetName_(domain)
            if newDomain:
                acceptedDomains.append(newDomain)
        return {'domains': acceptedDomains}

    def isComment_(self, line):
        if line.startswith('#'):
            return True
        return False