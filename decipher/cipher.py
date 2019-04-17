"""
cipher.py
For Decipher coding challenge
by Ben Pall

Represents a mapping from encoded letters to decoded letters. We also
store/maintain the inverted mapping."""

import string


class Cipher:
	def __init__(self):
		self.mapping = {}
		self.inverted_mapping = {}

	def __str__(self):
		s = ""
		for a in string.ascii_lowercase:
			if a not in self.mapping:
				continue
			else:
				s = s + a + " -> " + self.mapping[a] + '\n'
		return s[:-1]

	def get(self, a):
		if a in self.mapping:
			return self.mapping[a]
		else:
			return False

	def get_decode(self, b):
		if b in self.inverted_mapping:
			return self.inverted_mapping[b]
		else:
			return False

	def isMapped(self, a):
		return a in self.mapping


	def isMapped_decode(self, b):
		return b in self.inverted_mapping

	def isCompatible(self, chara, charb):
		"""Checks whether the given pair of characters conflicts with the mapping."""
		if self.isMapped(chara) and self.get(chara) is not charb:
			return False
		elif self.isMapped_decode(charb) and self.get_decode(charb) is not chara:
			return False
		else:
			return True

	def map(self, a, b):
		if self.isMapped(a) and self.get(a) is not b:
			print("Error: attempted to map a mapped character.")
			return False
		elif self.isMapped_decode(b) and self.get_decode(b) is not a:
			print("Error: attempted to map to a mapped character.")
			return False
		else:
			self.mapping[a] = b
			self.inverted_mapping[b] = a
			return True

	def unmap(self, a):
		if not self.isMapped(a):
			print("Error: attempted to unmap an unmapped character.")
			print(self.mapping)
			print(a)
			return False
		else:
			b = self.mapping.pop(a)
			self.inverted_mapping.pop(b)

	def map_batch(self, batch):
		"""Maps a batch of character pairs (also represented as a Cipher) in one shot."""
		for chara, charb in batch.get_mapping().items():
			self.map(chara, charb)

	def unmap_batch(self, batch):
		"""Unmaps a batch of character pairs (also represented as a Cipher) in one shot."""
		for chara, charb in batch.get_mapping().items():
			self.unmap(chara)

	def get_mapping(self, inverted=False):
		if inverted:
			return self.inverted_mapping
		else:
			return self.mapping

	def match_remaining_letters(self):
		"""Some letters of the alphabet may not appear in the messages at all, so their true
		pairings may be undeterminable. This function maps the unmapped letters arbitrarily
		for purposes of output, etc."""
		for a in string.ascii_lowercase:
			if a not in self.mapping:
				for b in string.ascii_lowercase:
					if b not in self.inverted_mapping:
						self.map(a,b)
						break 

