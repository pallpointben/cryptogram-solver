"""
decipher.py
For Decipher coding challenge
by Ben Pall
"""

import sys, json, pickle, time
import message
import util
from collections import Counter, defaultdict
from cipher import Cipher
import operator


corpus_file = 'data/corpus-en.txt'
input_file = 'input/encoded-en.txt'


def sort_by_pattern_uniqueness(messages):
	"""Rearranges the words in the message so that the words with the
	most unique patterns come first. This optimizes our depth-first search
	by ensuring that earlier nodes (i.e., words from the message) have 
	fewer branches (i.e., possible paired words from the corpus) to traverse."""
	return sorted(messages, key=lambda x: len(patterns[util.get_pattern(x)]))

def decipher(messages):
	"""Wrapper for the code cracking process. messages must be a cleaned and
	tokenized representation of the encoded messages."""
	return crack_code(messages, 0)

def crack_code(messages, tolerance):
	"""Attempts to crack the code starting with the first word in the (newly resorted
	by pattern uniqueness) message. Tolerance is introduced to account for words in the
	message that are not necessarily in the corpus. Tolerance is the number of message words we are allowed
	to ignore while mapping message words to corpus words. At first we tolerate none of these, because
	ideally all of the message words are common enough to be found in the corpus. If that fails,
	we try again but increase tolerance by one."""
	messages = sort_by_pattern_uniqueness(messages)
	code = Cipher()
	cipher_found = crack_word(code, messages, 0, tolerance)
	if cipher_found:
		return code
	elif tolerance < len(messages):
		return crack_code(messages, tolerance+1)
	else:
		quit("Error: No cipher found.")


def crack_word(code, messages, i, tolerance):
	"""Tries possible corpus-word matches for the ith word in the message."""
	worda = messages[i]
	for wordb in possible_matches(worda):
		if attempt_match(code, messages, i, wordb, tolerance):
			return True
	"""If we get here, there is no match compatible with our partial cipher. If we have
	tolerance to spare we can skip this word and keep trying. Otherwise return false- retrace
	our steps and pursue a different path."""
	if tolerance == 0:
		return False
	else:
		return crack_word(code, messages, i+1, tolerance-1)


def possible_matches(worda):
	"""Finds all possible matching corpus words- all words from the corpus with a matching
	letter pattern to the current word."""
	return patterns[util.get_pattern(worda)]

def attempt_match(code, messages, i, wordb, tolerance):
	"""Explores a corpus-word pair for the current message word. batch keeps track of which
	new letters are mapped under the assumption that wordb is a match for the ith message word."""
	batch = Cipher()
	worda = messages[i]
	for chara, charb in zip(worda, wordb):
		"""Checks if the new assumption would conflict with the current mapping. If it does,
		return False- i.e., try a different corpus word."""
		if not code.isCompatible(chara, charb) or not batch.isCompatible(chara, charb):
			return False
		elif not code.isMapped(chara) and not batch.isMapped(chara):
			batch.map(chara, charb)
	"""If we get here, it means that this word mapping is 
	compatible with our cipher so far and also internally.
	Map the new batch of letters (from the current word) in the cipher.
	If we made a mistake, we can unmap it later when we return to this layer of
	the recursion."""
	code.map_batch(batch)
	"""Check if we've reached the end of our message. 
	If so, we have found a complete compatible cipher. Otherwise,
	proceed to the next word."""
	if i >= len(messages) - 1:
		return True
	elif crack_word(code, messages, i+1, tolerance):
		return True
	else:
		code.unmap_batch(batch)
		return False



if __name__ == "__main__":

	starttime = time.time()
	if (len(sys.argv) > 2):
		quit("Error: too many arguments.")
	elif (len(sys.argv) == 2):
		input_file = sys.argv[1]

	try:
		print("Attempting to load preprocessed files...")
		with open('pickle/word_freqs.P', "rb") as f:
			word_freqs = pickle.load(f)
		with open('pickle/patterns.P', "rb") as f:
			patterns = pickle.load(f)

	except:		
		with open(corpus_file) as f:
			corpus = f.read()
		print("Load failed. Preprocessing corpus...")
		corpus = util.tokenize_and_clean(corpus)
		word_freqs = Counter(corpus)
		patterns = defaultdict(list)
		for word in sorted(word_freqs.keys(), key=lambda x: word_freqs[x], reverse=True):
			pattern = util.get_pattern(word)
			patterns[pattern].append(word)
		with open('pickle/word_freqs.P', "wb") as f:
			pickle.dump(word_freqs, f)
		with open('pickle/patterns.P', "wb") as f:
			pickle.dump(patterns, f)

	with open(input_file) as f:
		messages = message.message(f.read())
	print("Cracking code...")
	code = decipher(messages.tokenize_and_clean())
	code.match_remaining_letters()
	with open('output/cipher.txt', "w") as f:
		f.write(str(code))
	with open('output/decoded_messages.txt', "w") as f:
		f.write(messages.decode(code))
	print("Decoding complete.")
	endtime = time.time()
	print("Duration: " + str(endtime - starttime)[:5] + " seconds.")