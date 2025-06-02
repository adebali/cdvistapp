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
        {'start': 1, 'end': 30},
        {'start': 50, 'end': 100},
        {'start': 110, 'end': 160},
        {'start': 190, 'end': 200}
    ]
    assert domain2interval({'start': 10, 'end': 20}) == p.closed(10, 20)
    assert domains2intervalSet(proteinObject['segments']['assigned']) == set([p.closed(30,50), p.closed(100,110), p.closed(160,190)])
    assert getUnassignedSegments(proteinObject) == unassignedSegments

    originalInterval = p.closed(150, 250)
    subInterval = p.closed(10, 35)
    assert relativeIntervalTransform(originalInterval, subInterval) == p.closed(160, 185)

    originalDomain = {'start': 150, 'end': 250}
    subDomain = {'start': 10, 'end': 35, 'anotherField': 'exists'}
    assert relativeDomainTransform(originalDomain, subDomain) == {'start': 160, 'end': 185, 'anotherField': 'exists'}


