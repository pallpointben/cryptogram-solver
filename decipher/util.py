"""
util.py
For Decipher coding challenge
by Ben Pall"""

from nltk import tokenize
import re

def tokenize_and_clean(string):
	"""Exactly what it says on the tin."""
	string = string.lower().replace('-', ' ')
	string = tokenize.word_tokenize(string)
	string = ["".join([char for char in word if char.isalpha()]) for word in string]
	return string

def get_pattern(word):
	"""Words -> patterns are many-to-one. A pattern is an internally consistent
	representation of word in terms of which letters are the same/different.
	E.g., "apple" and "peers" have the same pattern because they both map to the pattern
	"abbcd". Non alphabetic characters are left alone. Useful for quickly determining 
	which corpus words are a possible match for a given message word."""
	curralpha = 'a'
	pattern = ""
	mapping = {}
	for letter in word:
		if letter.isalpha():
			if letter not in mapping:
				mapping[letter] = curralpha
				curralpha = chr(ord(curralpha) + 1)
			pattern = pattern + mapping[letter]
		else:
			pattern = pattern + letter
	return pattern
