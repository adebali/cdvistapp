from ..unassigned import *

def test_intervals():
    proteinObject = {
        'length': 200,
        'segments': {
            'assigned':
                [
                    {'start': 30, 'end': 50},
                    {'start': 100, 'end': 110},
                    {'start': 160, 'end': 190}
                ]
        }
    }
    unassignedSegments = [
        {'start': 1, 'end': 29},
        {'start': 51, 'end': 99},
        {'start': 111, 'end': 159},
        {'start': 191, 'end': 200}
    ]
    assert domain2interval({'start': 10, 'end': 20}) == p.closed(10, 20)
    assert domains2intervalSet(proteinObject['segments']['assigned']) == p.closed(30,50) | p.closed(100,110) | p.closed(160,190)
    assert getUnassignedSegments(proteinObject) == unassignedSegments

    originalInterval = p.closed(150, 250)
    subInterval = p.closed(10, 35)
    assert relativeIntervalTransform(originalInterval, subInterval) == p.closed(159, 184)

    originalDomain = {'start': 150, 'end': 250}
    subDomain = {'start': 10, 'end': 35, 'anotherField': 'exists'}
    assert relativeDomainTransform(originalDomain, subDomain) == {'start': 159, 'end': 184, 'anotherField': 'exists'}


