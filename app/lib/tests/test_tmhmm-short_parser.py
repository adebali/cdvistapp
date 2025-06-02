#!/usr/bin/python
import os
import re
from ..utils import jsonFile2dict
from ..tmhmm_short_parser import TMHMMresult

def test_TMHMMresult():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')        
    tmhmm_short_result = TMHMMresult(os.path.join(testDataDir, 'tmhmm-short_results.txt'))
    expectedDomains = jsonFile2dict(os.path.join(testDataDir, 'tmhmm-short_results.json'))
    assert tmhmm_short_result.results == expectedDomains
