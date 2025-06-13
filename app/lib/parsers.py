#!/usr/bin/env python

import os
import sys
import json

def tmhmm(requestJson, filename, toolIndex):
    from tmhmm_short_parser import TMHMMresult
    toolJob = requestJson['tools'][toolIndex]
    output = TMHMMresult(filename)
    queries = output.results

    i = 0
    for protein in queries:
        requestJson['entries'][i]['tm'] = protein['domains']
        i += 1
    return requestJson

def deepTMHMM(requestJson, filename, toolIndex):
    from deepTMHMM_gff3_parser import deepTMHMM
    toolJob = requestJson['tools'][toolIndex]
    output = deepTMHMM(filename)
    queries = output

    i = 0
    for protein in queries:
        usedDomains = []
        for domain in protein['domains']:
            if domain['name'] == 'TMhelix':
                usedDomains.append(domain)
        requestJson['entries'][i]['tm'] = usedDomains
        i += 1
    return requestJson

def hmmer(requestJson, filename, toolIndex):
    from hmmscan_parser import HmmscanResult
    toolJob = requestJson['tools'][toolIndex]
    output = HmmscanResult(filename)
    queries = output.results

    i = 0
    for protein in queries:
        hits = protein['domains']

        for hit in hits:
            segment = {
                'name'      : hit['name'],
                'start'     : hit['env_from'],
                'end'       : hit['env_to'],
                'score'     : hit['score'],
                'cov'       : hit['hmm_cov'],
                'prob'      : 'NaN',
                'assigned'  : True,
                'tool'  : {
                    'name'  : toolJob['name'],
                    'db'    : toolJob['db'],
                    'meta'  : hit
                }
            }

            requestJson['entries'][i]['segments']['assigned'].append(segment)
        i += 1
    
    return requestJson

def hhsearch(filename, toolJob):
    from hhsearch_parser import HHsearchResult

    def measureCov(coverageString, hmmLength):
        fullCoverageCutoff = 0.05
        coverage = ''
        coverageList = coverageString.split('-')
        start = int(coverageList[0])
        end = int(coverageList[1])
        if start == 1 or float(start)/hmmLength < fullCoverageCutoff:
            coverage += '['
        else:
            coverage += '.'

        if end == hmmLength or (hmmLength - end)/float(hmmLength) < fullCoverageCutoff:
            coverage += ']'
        else:
            coverage += '.'
        return coverage

    adaptedDomains = []
    results = HHsearchResult(filename).getResults()
    domains = results['domains']
    for domain in domains:
        queryIntervalList = domain['query'].split('-')
        segment = {
            'name'      : domain['hit'],
            'start'     : int(queryIntervalList[0]),
            'end'       : int(queryIntervalList[1]),
            'score'     : float(domain['score']),
            'cov'       : measureCov(domain['template'], domain['hmm']),
            'prob'      : float(domain['prob']),
            'assigned'  : None,
            'tool'  : {
                'name'  : toolJob['name'],
                'db'    : toolJob['db'],
                'meta'  : domain
            }
        }
        adaptedDomains.append(segment)
    return adaptedDomains

# def hhblits(filename, toolJson):
#     return toolJson

def rpsblast(filename, toolJob, bitScoreFile):
    from rpsblast_outfmt7_parser import RpsblastResult

    def measureCov(start, end, modelLength):
        fullCoverageCutoff = 0.05
        coverage = ''
        if start == 1 or float(start)/modelLength < fullCoverageCutoff:
            coverage += '['
        else:
            coverage += '.'

        if end == modelLength or (modelLength - end)/float(modelLength) < fullCoverageCutoff:
            coverage += ']'
        else:
            coverage += '.'
        return coverage

    adaptedDomains = []
    results = RpsblastResult(filename, bitScoreFile).getResults()
    domains = results['domains']
    for domain in domains:
        start = int(domain['q. start'])
        end = int(domain['q. end'])
        segment = {
            'name'  : domain['subject acc.ver'],
            'start' : start,
            'end'   : end,
            'score' : float(domain['bit score']),
            'cov'   : measureCov(start, end, domain['alignment length']),
            'evalue': float(domain['evalue']),
            'prob'  : None,
            'assigned': True,
            'tool'  : {
                'name'  : toolJob['name'],
                'db'    : toolJob['db'],
                'meta'  : domain
            }
        }
        adaptedDomains.append(segment)
    return adaptedDomains

def tmPrediction(filename, toolJson):
    return toolJson

