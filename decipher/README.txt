Overview
---------------
This program deciphers messages encoded in a simple alphabetic substitution cipher, given a corpus of English-language books.

Instructions
---------------
To run the program, type "python decipher.py" into the command line. An optional argument specifies the path of the encoded message. If it is not provided, the default path (specified in the main file) will be used.

Requirements and Dependencies
---------------
This program was built in Python 3. It has not been tested on
Python 2. Only standard Python libraries are used, with the exception of nltk, which is used only for its word_tokenize() function.

Approach
---------------
I approached my design, at a high level, as a depth-first search over the space of mappings from words in the provided messages to the words in the corpus. If implemented naively, this search would take extremely long in the average case. However, I have introduced several optimizations to the approach:

 * For each word in the message, I only search over the words in the corpus with a matching letter pattern (for more information on letter patterns, see util.py).

 * I rearrange the words in the message so that the words with the most unique patterns come first. This optimizes the depth-first search by ensuring that earlier nodes (i.e., words from the message) have fewer branches (i.e., possible paired words from the corpus) to traverse.

* For each word in the message, I search possible corpus-word matches in descending order of corpus word frequency, so that more common words are examined first.

I also introduce a tolerance factor to account for words in the message that are not necessarily in the corpus. Tolerance is the number of message words we are allowed to ignore while mapping message words to corpus words. At first we tolerate none of these, because ideally all of the message words are common enough to be found in the corpus. If that fails, we try again but increase tolerance by one.

Future Work
---------------
I began this project under the assumption that all words in the message would always appear in the corpus. Upon discovering that that assumption did not hold, I introduced the tolerance factor to support words that did not appear in the corpus. If I could begin this project again or if I had more time, I might try to replace my depth first search approach with a statistical approach over letter mappings, using corpus letter/word frequencies in my analysis. Still, I am impressed with the simplicity and performance of my approach, and it may well be the best approach to this problem.