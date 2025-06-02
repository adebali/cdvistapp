import os
from ..fasta import fasta

def test_fasta():
    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')        
    fastaObject = fasta(os.path.join(testDataDir, 'fasta-test.fa'))
    assert fastaObject.getMaxSeqLength() == 15
    assert fastaObject.getSequenceCount() == 2

    testDataDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test-data')        
    fastaObject = fasta(os.path.join(testDataDir, 'fasta-test.2.fa'))
    for seqObject in fastaObject.stream():
        assert seqObject.getLength() == 2466
        assert len(seqObject.getSequence()) == 2466
        assert seqObject.getHeader() == '>ref|XP_023931987.1| uncharacterized protein LOC106169985 [Lingula anatina]'
