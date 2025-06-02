import os
from ..utils import jsonFile2dict

def test_jsonFile2dict():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')        
    jsonFile = os.path.join(testDataDir, 'json.json')
    expectedResults = {'a':1, 'b':2, 'c': {'a': 1, 'b':2}}
    assert jsonFile2dict(jsonFile) == expectedResults

