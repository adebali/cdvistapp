import os
import json
from lib import fasta

def makeJson(id, inputFile, tools):
    jobs = []
    fastaObject = fasta.fasta(inputFile)
    for seqObject in fastaObject.stream():
        seqLength = len(seqObject.getSequence())
        jobItem = {
            'header': fasta.cleanUpTrailing(seqObject.getHeader()),
            'sequence': fasta.cleanUpTrailing(seqObject.getSequence()),
            'length': seqLength,
            'segments': {
                'orphan': [[1, seqLength]],
                'assigned': [],
                'unassigned': []
            },
            'tm': [],
            'coils': [],
            'lcr': [],
            'status': 'pending'
        }
        jobs.append(jobItem)
    outputFile = os.path.join(os.path.dirname(inputFile), 'request.json')

    request = {
        'entries': jobs,
        'tools': tools,
        'id': id
    }
    with open(outputFile, 'w') as fp:
        json.dump(request, fp, indent=1, sort_keys=True)

    return request

if __name__ == "__main__":
    import sys
    tools = {}
    makeJson(sys.argv[1], sys.argv[2], tools)
