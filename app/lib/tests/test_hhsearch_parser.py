#!/usr/bin/python
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from hhsearch_parser import HHsearchResult
from utils import jsonFile2dict

def test_hhsearchResult():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')        
    hhsearch_result = HHsearchResult(os.path.join(testDataDir, 'hhsearch-results.txt'))
    expectedDomains = jsonFile2dict(os.path.join(testDataDir, 'hhsearch-results.json'))
    assert hhsearch_result.getResults()['domains'][0] == expectedDomains['domains'][0]

    hhsearch_result = HHsearchResult(os.path.join(testDataDir, 'hhsearch-results-case1.txt'))
    expectedDomains = jsonFile2dict(os.path.join(testDataDir, 'hhsearch-results-case1.json'))
    assert hhsearch_result.getResults()['domains'] == expectedDomains['domains']

    void_hhsearch_result = HHsearchResult(os.path.join(testDataDir, 'hhsearch-results-void.txt'))
    expectedDomains = jsonFile2dict(os.path.join(testDataDir, 'hhsearch-results-void.json'))
    assert void_hhsearch_result.getResults()['domains'] == expectedDomains['domains']
