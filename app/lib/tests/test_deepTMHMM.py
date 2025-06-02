import biolib
import os
from ..utils import jsonFile2dict
from ..deepTMHMM_3line_parser import deepTMHMMresult

# app = biolib.load('DTU/DeepTMHMM:1.0.24')

# Run the application locally on your FASTA file
# result = app.cli(args='--fasta test-data/fasta-test.2.fa', machine='local')

# Access the results
# result.save_files('test-data/deepTMHMM_results')


def test_deepTMHMMresult():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data') 
    deepTMHMM = deepTMHMMresult(os.path.join(testDataDir,'deepTMHMM_results', 'predicted_topologies.3line'))
    expectedDomains = jsonFile2dict(os.path.join(testDataDir, 'tmhmm-short_results.json'))
    assert deepTMHMM.results == expectedDomains
