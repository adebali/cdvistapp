#!/usr/bin/python
import os
import re

class HHsearchResult():
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.query = {'domains':[]}
    def parseHitLine_(self, line):
    # Example Line
    #  1 UP20|NICMADEBA|992|408 Ethanol 100.0 4.9E-42 5.4E-47  308.4   0.0  219    3-222    68-290 (408)

        hitName = line[4:34]
        fields = ' '.join(line.split(hitName)).split()
        no = int(fields[0])
        probability = float(fields[1])
        evalue = float(fields[2])
        pvalue = float(fields[3])
        score = float(fields[4])
        ss = float(fields[5])
        cols = int(fields[6])
        query = fields[7]
        template = fields[8].split('(')[0]
        if len(fields) >= 10:
            HMM = int(fields[9].replace('(', '').replace(')', ''))
        else:
            HMM = int(fields[8].split('(')[1].replace(')', ''))            
        return {
            'no': no,
            'hit': hitName,
            'prob': probability,
            'evalue': evalue,
            'pvalue': pvalue,
            'score': score,
            'ss': ss,
            'cols': cols,
            'query': query,
            'template': template,
            'hmm': HMM
        }

    def saveQueryInfo_(self, queryInfo):
        self.query['name'] = queryInfo['Query']
        # self.query['length'] = int(queryInfo['Match_columns'])
        return self

    def parse_(self):
        informationLines = True
        hitsStarted = False
        queryInfo = {}
        filein = open(self.inputFile ,'r')
        for line in filein:
            if line.strip() != '' and informationLines == True:
                queryInfo[line.strip()[:14].strip()] = line.strip()[15:]
            else:
                informationLines = False
                if not hitsStarted:
                    self.saveQueryInfo_(queryInfo)

            if line.strip().startswith('No '):
                hitsStarted = True

            if informationLines == False and line.strip() != '' and (not line.strip().startswith('No')):
                featureObject = self.parseHitLine_(line)
                self.query['domains'].append(featureObject)
                
            if informationLines == False and line.strip() == '' and hitsStarted:
                return self

    def getResults(self):
        self.parse_()
        return self.query
