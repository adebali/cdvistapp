#!/usr/bin/env python

class seq:
	def __init__(self, input, up=True):
		self.sequence_ = input.strip()
		if up:
			self.sequence_ = self.sequence_.upper()
		self.header_ = None

	def subseq(self, start, end):
		# Zero-based subsequence function
		return seq(self.sequence_[start : end])

	def assignHeader(self, header):
		self.header_ = header

	def getHeader(self):
		return self.header_

	def getLength(self):
		return len(self.getSequence())

	def getSequence(self):
		return self.sequence_


