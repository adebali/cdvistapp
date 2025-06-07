#!/usr/bin/env python

import unittest
from unassigned import getUnassignedSegments, relativeDomainTransform
from seq import seq
import copy
from time import sleep

def updateProteinWithNewDomains(proteinObject, segment, partialProteinObject):
    transformedSegments = []
    for domain in partialProteinObject['segments']['assigned']:
        transformedSegments.append(relativeDomainTransform(segment, domain))
    proteinObject['segments']['assigned'] += transformedSegments
    proteinObject['segments']['assigned'] = sorted(proteinObject['segments']['assigned'], key=lambda k: k['start'])
    return proteinObject

def runSingleProtein(proteinObject, toolJob, callFunction):
    gapLengthCutoff = int(toolJob['gap_length'])
    voidSet = set()
    def iterateSegments(proteinObject, gapLengthCutoff, callFunction):
        proteinSequence = seq(proteinObject['sequence'])
        unassignedSegments = getUnassignedSegments(proteinObject)
        print('Unassigned segments:', unassignedSegments)
        for segment in unassignedSegments:
            subSequence = proteinSequence.subseq(segment['start'] - 1, segment['end']).getSequence()
            segmentLength = segment['end'] - segment['start']
            segmentInterval = str(segment['start']) + '..' + str(segment['end'])
            if (segmentInterval not in voidSet) and segmentLength >= gapLengthCutoff:
                partialProteinObject = {
                    'sequence': subSequence,
                    'length': segmentLength,
                    'segments': {
                        'assigned': []
                    }
                }
                domains = callFunction(subSequence, segment, toolJob)
                print('Domains found:', domains)
                if domains != []:
                    partialProteinObject['segments']['assigned'] = domains
                    proteinObject = updateProteinWithNewDomains(proteinObject, segment, partialProteinObject)
                    proteinObject = iterateSegments(proteinObject, gapLengthCutoff, callFunction)
                voidSet.add(segmentInterval)
            else:
                voidSet.add(segmentInterval)
        return proteinObject

    finalProteinObject = iterateSegments(proteinObject, gapLengthCutoff, callFunction)
    # print(finalProteinObject)
    return finalProteinObject


