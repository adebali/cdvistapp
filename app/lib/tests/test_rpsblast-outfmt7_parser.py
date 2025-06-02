#!/usr/bin/python
import os
from ..rpsblast_outfmt7_parser import RpsblastResult
from ..utils import jsonFile2dict
import json


def test_rpsblastResult():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')        
    rpsblast_result = RpsblastResult(os.path.join(testDataDir, 'rpsblast-results.txt'), os.path.join(testDataDir, 'bitscore_specific_3.16.txt'))
    expectedDomains = jsonFile2dict(os.path.join(testDataDir, 'rpsblast-results.json'))
    assert rpsblast_result.getResults() == expectedDomains

    rpsblast_result = RpsblastResult(os.path.join(testDataDir, 'rpsblast-results-void.txt'), os.path.join(testDataDir, 'bitscore_specific_3.16.txt'))
    expectedDomains = jsonFile2dict(os.path.join(testDataDir, 'rpsblast-results-void.json'))
    assert rpsblast_result.getResults() == expectedDomains