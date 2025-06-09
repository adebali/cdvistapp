import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from iterativeSubSequenceSearch import *
import pytest
import copy

exampleProteinObject = {
    'sequence': 'A'*240,
    'length': 240,
    'segments': {
        'assigned': [
            {'start': 100, 'end': 200}
        ],
        'unassigned': []
    }
}

exampleProteinObject2 = {
    'sequence': 'A'*20,
    'length': 20,
    'segments': {
        'assigned': [
            {'start': 5, 'end': 10},
            {'start': 17, 'end': 20}
        ],
        'unassigned': []
    }
}

toolJob = {'gap_length': 30, 'db': 'pfam31', 'prob': 0.60}

# @pytest.mark.skip()
def test_iterate():
    def pseudoDomainFinder(subSequence, segment, toolJob):
        if segment['start'] == 240:
            return []
        return [
            {'start': 10, 'end': 40}
        ]
    
    def pseudoDomainFinder2(subSequence, segment, toolJob):
        return [
            {'start': 2, 'end': 4}
        ]
    proteinObject = copy.deepcopy(exampleProteinObject)
    toolJob = {'gap_length': 30, 'db': 'pfam31', 'prob': 0.60}
    result = runSingleProtein(proteinObject, toolJob, pseudoDomainFinder)
    expectedResult = copy.deepcopy(proteinObject)
    expectedResult['segments']['assigned'] = [{'start': 10, 'end': 40}, {'start': 50, 'end': 80}, {'start': 100, 'end': 200}, {'start': 210, 'end': 240}]
    assert result == expectedResult

    toolJob = {'gap_length': 2, 'db': 'pfam31', 'prob': 0.60}
    proteinObject = copy.deepcopy(exampleProteinObject2)
    result = runSingleProtein(proteinObject, toolJob, pseudoDomainFinder2)
    expectedResult = copy.deepcopy(proteinObject)
    expectedResult['segments']['assigned'] = [{'start': 2, 'end': 4}, {'start': 5, 'end': 10}, {'start': 12, 'end': 14}, {'start': 17, 'end': 20}]
    assert result == expectedResult

def test_voidIterate():
    def pseudoDomainFinder(subSequence, segment, toolJob):
        return []
    proteinObject = copy.deepcopy(exampleProteinObject)
    result = runSingleProtein(proteinObject, toolJob, pseudoDomainFinder)
    expectedResult = copy.deepcopy(proteinObject)
    assert result == expectedResult

def test_updateProteinWithNewDomains():
    proteinObject = copy.deepcopy(exampleProteinObject)
    partialProteinObject = {
        'segments': {
            'assigned': [
                {'start': 10, 'end': 20, 'anotherFied': 'field'},
                {'start': 30, 'end': 59, 'anotherFied': 'field2'}
            ]
        }
    }
    segment = {'start': 220, 'end': 290}
    expectedResult = copy.deepcopy(proteinObject)
    expectedResult['segments']['assigned'].insert(1, {'start': 249, 'end': 278, 'anotherFied': 'field2'})
    expectedResult['segments']['assigned'].insert(1, {'start': 229, 'end': 239, 'anotherFied': 'field'})
    assert set(updateProteinWithNewDomains(proteinObject, segment, partialProteinObject)) == set(expectedResult)


# test_iterate()