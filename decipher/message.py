"""
message.py
For Decipher coding challenge
by Ben Pall

Represents an encoded message, with some useful functions."""



import string
from cipher import Cipher
import util


class message:

	def __init__(self, msg):
		self.text = msg

	def tokenize_and_clean(self):
		return util.tokenize_and_clean(self.text)

	def decode(self, cipher):
		"""Applies the given cipher to the encoded message."""
		def decode_c(cipher, c):
			if c.isalpha():
				if c.isupper():
					return cipher.get(c.lower()).upper()
				else:
					return cipher.get(c)
			else:
				return c
		return "".join([decode_c(cipher, c) for c in self.text])


# Unit Test
if __name__ == "__main__":
	msg = "Lkccz mzfca."
	mapping = {'a': 'd', 'k': 'e', 'l': 'h', \
					'c': 'l', 'z': 'o', 'f': 'r', 'm': 'w'}
	code = Cipher()
	code.mapping = mapping

	coded_message = message(msg)
	print("\nTokenize message:\n" + str(coded_message.tokenize_and_clean()) + "\n")
	print("Decipher message:\n" + coded_message.decode(code) + "\n")