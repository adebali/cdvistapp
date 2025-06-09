import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from iterativeSubSequenceSearch import *
import copy

exampleProteinObject2 = {
    'sequence': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'length': 26,
    'segments': {
        'assigned': [
            {'start': 5, 'end': 10},
            {'start': 17, 'end': 20}
        ],
        'unassigned': []
    }
}


# @pytest.mark.skip()
def test_iterate():
    
    def pseudoDomainFinder2(subSequence, segment, toolJob):
        return [
            {'start': 2, 'end': 4}
        ]

    toolJob = {'gap_length': 2, 'db': 'pfam31', 'prob': 0.60}
    proteinObject = copy.deepcopy(exampleProteinObject2)
    result = runSingleProtein(proteinObject, toolJob, pseudoDomainFinder2)
    # print(result)
    expectedResult = copy.deepcopy(proteinObject)
    expectedResult['segments']['assigned'] = [{'start': 2, 'end': 4}, {'start': 5, 'end': 10}, {'start': 12, 'end': 14}, {'start': 17, 'end': 20}, {'start': 22, 'end': 24}]
    assert result == expectedResult