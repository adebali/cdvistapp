from ..iterativeSubSequenceSearch import *
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

toolJob = {'gap_length': 30, 'db': 'pfam31', 'prob': 0.60}

# @pytest.mark.skip()
def test_iterate():
    def pseudoDomainFinder(subSequence, segment, toolJob):
        if segment['start'] == 240:
            return []
        return [
            {'start': 10, 'end': 40}
        ]
    proteinObject = copy.deepcopy(exampleProteinObject)
    result = runSingleProtein(proteinObject, toolJob, pseudoDomainFinder)
    expectedResult = copy.deepcopy(proteinObject)
    expectedResult['segments']['assigned'] = [{'start': 11, 'end': 41}, {'start': 51, 'end': 81}, {'start': 100, 'end': 200}, {'start': 210, 'end': 240}, 
    # {'start': 250, 'end': 280},
    # {'start': 290, 'end': 320},
    # {'start': 330, 'end': 360},
    # {'start': 370, 'end': 400},
    # {'start': 410, 'end': 440},
    # {'start': 450, 'end': 480},
    # {'start': 490, 'end': 520},
    # {'start': 530, 'end': 560},
    # {'start': 570, 'end': 600},
    {'start': 600, 'end': 700}, {'start': 710, 'end': 740}, {'start': 750, 'end': 780}, {'start': 790, 'end': 820}, {'start': 830, 'end': 860}, {'start': 870, 'end': 900}, {'start': 910, 'end': 940}, {'start': 950, 'end': 980}]

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
    expectedResult['segments']['assigned'].insert(1, {'start': 250, 'end': 279, 'anotherFied': 'field2'})
    expectedResult['segments']['assigned'].insert(1, {'start': 230, 'end': 240, 'anotherFied': 'field'})
    print(expectedResult)
    assert updateProteinWithNewDomains(proteinObject, segment, partialProteinObject) == expectedResult


