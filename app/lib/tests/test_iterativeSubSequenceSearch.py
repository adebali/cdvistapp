import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from iterativeSubSequenceSearch import *
import pytest
import copy

exampleProteinObject = {
    'sequence': 'A'*124 + '1' + 'A'*124 + '2' + 'T'*124 + '3' + 'T'*124 + '4' + 'C'*124 + '5' + 'C'*124 + '6' + 'G'*124 + '7' + 'G'*124 + '8',
    'length': 1000,
    'segments': {
        'assigned': [
            {'start': 100, 'end': 200},
            {'start': 600, 'end': 700}
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
    expectedResult['segments']['assigned'] = [{'start': 10, 'end': 40}, {'start': 50, 'end': 80}, {'start': 100, 'end': 200}, {'start': 210, 'end': 240}, 
    {'start': 600, 'end': 700}, {'start': 710, 'end': 740}, {'start': 750, 'end': 780}, {'start': 790, 'end': 820}, {'start': 830, 'end': 860}, {'start': 870, 'end': 900}, {'start': 910, 'end': 940}, {'start': 950, 'end': 980}]
    # assert result == expectedResult

    toolJob = {'gap_length': 2, 'db': 'pfam31', 'prob': 0.60}
    proteinObject = copy.deepcopy(exampleProteinObject2)
    result = runSingleProtein(proteinObject, toolJob, pseudoDomainFinder2)
    print(result)
    expectedResult = copy.deepcopy(proteinObject)
    expectedResult['segments']['assigned'] = [{'start': 2, 'end': 4}, {'start': 6, 'end': 8}, {'start': 10, 'end': 15}]
    # assert result == expectedResult

def test_voidIterate():
    def pseudoDomainFinder(subSequence, segment, toolJob):
        return []
    proteinObject = copy.deepcopy(exampleProteinObject)
    result = runSingleProtein(proteinObject, toolJob, pseudoDomainFinder)
    expectedResult = copy.deepcopy(proteinObject)
    # assert result == expectedResult

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
    expectedResult['segments']['assigned'].insert(1, {'start': 250, 'end': 279, 'anotherFied': 'field2'})
    expectedResult['segments']['assigned'].insert(1, {'start': 230, 'end': 240, 'anotherFied': 'field'})
    # print(expectedResult)
    # assert updateProteinWithNewDomains(proteinObject, segment, partialProteinObject) == expectedResult


test_iterate()