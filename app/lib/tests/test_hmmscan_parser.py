#!/usr/bin/python
import os
import re
from ..utils import jsonFile2dict
from ..hmmscan_parser import HmmscanResult

def test_hmmscanResult():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')        
    hmmscan_result = HmmscanResult(os.path.join(testDataDir, 'hmmscan-results.txt'))
    expectedDomains = jsonFile2dict(os.path.join(testDataDir, 'hmmscan-results.json'))
    assert hmmscan_result.results[0]['domains'][0]['acc'] == 0.95
    assert hmmscan_result.results == expectedDomains
