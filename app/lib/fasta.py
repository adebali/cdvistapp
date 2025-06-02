#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.dirname(__file__))
import seq

class fasta:
    def __init__(self, input):
        self.file = input

    def stream(self, bufsize=4096*64*64):
        def chunk2seqDict(chunk):
            lines = chunk.split('\n')
            header = lines[0]
            del lines[0]
            sequence = ''.join(lines)
            seqObject = seq.seq(sequence)
            seqObject.assignHeader(header)
            return seqObject

        # Use 'with' statement and 'r' mode for file handling
        with open(self.file, 'r', encoding='utf-8') as filein:
            delimiter = '\n>'
            buf = ''
            justStarted = True
            while True:
                newbuf = filein.read(bufsize)
                if not newbuf:
                    if buf:  # Ensure the last chunk is processed
                        yield chunk2seqDict(buf)
                    return
                buf += newbuf
                sequenceChunks = buf.split(delimiter)
                for chunk in sequenceChunks[0:-1]:
                    if justStarted and chunk.startswith('>'):
                        chunk = chunk[1:]
                        justStarted = False
                    yield chunk2seqDict(chunk)
                buf = sequenceChunks[-1]
            
    def getSequenceCount(self):
        i = 0
        for seqObject in self.stream():
            i += 1
        return i

    def getMaxSeqLength(self):
        maxLength = 0
        for seqObject in self.stream():
            maxLength = max(maxLength, seqObject.getLength())
        return maxLength


def cleanUpTrailing(string):
    return string.replace('\r', '')