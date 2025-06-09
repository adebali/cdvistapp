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
    """Search unassigned segments of a protein for additional domains.

    Each unassigned region that is at least ``toolJob['gap_length']`` residues
    long is passed to ``callFunction``.  Domains returned by ``callFunction`` are
    converted to absolute coordinates and appended to
    ``proteinObject['segments']['assigned']``.  Newly assigned domains may split
    existing unassigned regions, therefore the search continues until all
    segments have been examined or fall below the size threshold.  Already
    processed intervals are tracked to prevent repeated searches.

    Args:
        proteinObject (dict): Protein record with ``sequence`` and segment
            information.
        toolJob (dict): Tool configuration.  ``gap_length`` is the minimum size
            of an unassigned region to be searched.
        callFunction (Callable[[str, dict, dict], list]): Function invoked on
            each subsequence to discover domains.  It should return a list of
            domain dictionaries.

    Returns:
        dict: Updated protein object including any new domains discovered.
    """

    gapLengthCutoff = int(toolJob['gap_length'])
    voidSet = set()
    proteinSequence = seq(proteinObject['sequence'])

    while True:
        unassignedSegments = getUnassignedSegments(proteinObject)
        print('Unassigned segments:', unassignedSegments)
        new_domain_found = False
        for segment in unassignedSegments:
            segmentLength = segment['end'] - segment['start']
            segmentInterval = f"{segment['start']}..{segment['end']}"
            if segmentInterval in voidSet or segmentLength < gapLengthCutoff:
                voidSet.add(segmentInterval)
                continue

            subSequence = proteinSequence.subseq(segment['start'] - 1, segment['end']).getSequence()
            domains = callFunction(subSequence, segment, toolJob)
            print('Domains found:', domains)
            voidSet.add(segmentInterval)
            if domains:
                partialProteinObject = {
                    'sequence': subSequence,
                    'length': segmentLength,
                    'segments': {'assigned': domains},
                }
                proteinObject = updateProteinWithNewDomains(proteinObject, segment, partialProteinObject)
                new_domain_found = True
                break
        if not new_domain_found:
            break


    return proteinObject


