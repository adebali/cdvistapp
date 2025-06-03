import os
from ..utils import jsonFile2dict

def test_jsonFile2dict():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')        
    jsonFile = os.path.join(testDataDir, 'json.json')
    expectedResults = {b'a':1, b'b':2, b'c': {b'a': 1, b'b':2}}
    assert jsonFile2dict(jsonFile) == expectedResults

