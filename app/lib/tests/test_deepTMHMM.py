import biolib
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import jsonFile2dict
from deepTMHMM_gff3_parser import deepTMHMM

# app = biolib.load('DTU/DeepTMHMM:1.0.24')

# Run the application locally on your FASTA file
# result = app.cli(args='--fasta test-data/fasta-test.2.fa', machine='local')

# Access the results
# result.save_files('test-data/deepTMHMM_results')


def test_deepTMHMM():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data') 
    deepTMHMMobject = deepTMHMM(os.path.join(testDataDir,'deepTMHMM_results', 'TMRs.gff3'))
    expectedDomains = jsonFile2dict(os.path.join(testDataDir, 'deepTMHMM_gff3_results.json'))
    print(deepTMHMMobject.results)
    assert set(deepTMHMMobject.results) == set(expectedDomains)

test_deepTMHMM()