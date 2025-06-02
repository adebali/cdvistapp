from ..seq import seq

def test_subseq():
	sequence = seq('AATTTAGCGTTAGCTGCTTTT')	
	assert sequence.subseq(2, 5).getSequence() == 'TTT'


