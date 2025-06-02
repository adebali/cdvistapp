import os
from ..parsers import hhsearch 
from ..hhsearch_parser import HHsearchResult
from ..rpsblast_outfmt7_parser import RpsblastResult

def test_hhsearch():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')
    hhsearch_result = HHsearchResult(os.path.join(testDataDir, 'hhsearch-results.txt'))
    domains = hhsearch_result.getResults()['domains']
    toolJob = {
        'name': 'myToolName',
        'db': 'myDatabase'
    }
    expectedDomain = {
        'name'  : 'PF05462.10 ; Dicty_CAR ; Slime',
        'start' : 409,
        'end'   : 729,
        'score' : 236.7,
        'cov'   : '[]',
        'prob'  : 99.8,
        'assigned': None,
        'tool'  : {
            'name'  : 'myToolName',
            'db'    : 'myDatabase',
            'meta'  : domains[0]
        }
    }

    assert expectedDomain == hhsearch(os.path.join(testDataDir, 'hhsearch-results.txt'), toolJob)[0]

    def test_rpsblast():
        testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')
        rpsblast_result = RpsblastResult(os.path.join(testDataDir, 'rpsblast-results.txt'))
        domains = rpsblast_result.getResults()['domains']
        toolJob = {
            'name': 'myToolName',
            'db': 'myDatabase'
        }
        expectedDomain = {
            'name'  : 'smart00342',
            'start' : 225,
            'end'   : 309,
            'score' : 76.1,
            'cov'   : '[]',
            'prob'  : None,
            'evalue'  : 1.3e-19,
            'assigned'  : True,
            'tool'  : {
                'name'  : 'myToolName',
                'db'    : 'myDatabase',
                'meta'  : domains[0]
            }
        }

        assert expectedDomain == rpsblast(os.path.join(testDataDir, 'rpsblast-results.txt'), toolJob)[0]