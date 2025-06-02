#!/usr/bin/env python

import portion as p

def domain2interval(domain):
    return p.closed(domain['start'], domain['end'])

def domains2intervalSet(domains):
    intervals = p.empty()
    for domain in domains:
        intervals |= domain2interval(domain)
    return set(intervals)

def intervals2unassignedSegments(intervals, intervalLengthCutoff=0):
    unassignedSegments = []
    for interval in intervals.items():
        intervalLength = interval.upper - interval.lower + 1
        if intervalLength > intervalLengthCutoff:
            unassignedSegments.append({
                'start': interval.lower,
                'end': interval.upper
            })
    return unassignedSegments

def getUnassignedSegments(proteinObject, gapLength=0):
    length = proteinObject['length']
    domains = proteinObject['segments']['assigned']
    proteinInterval = p.closed(1, length)
    domainIntervals = domains2intervalSet(domains)
    unassignedIntervals = proteinInterval - domainIntervals
    unassignedSegments = intervals2unassignedSegments(unassignedIntervals, gapLength)
    return unassignedSegments

def relativeIntervalTransform(originalInterval, subInterval):
    originalLowerBound = originalInterval.lower
    absInterval = p.closed(
        originalLowerBound + subInterval.lower,
        originalLowerBound + subInterval.upper
    )
    return absInterval

def relativeDomainTransform(originalDomain, subDomain):
    start1 = originalDomain['start']
    end1 = originalDomain['end']
    start2 = subDomain['start']
    end2 = subDomain['end']
    transformedInterval = relativeIntervalTransform(p.closed(start1, end1), p.closed(start2, end2))
    newDomain = subDomain.copy()
    newDomain['start'] = transformedInterval.lower
    newDomain['end'] = transformedInterval.upper
    return newDomain
