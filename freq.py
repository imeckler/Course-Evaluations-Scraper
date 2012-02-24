#!/usr/bin/python
import sys
import string

# a string consisting of as many spaces as there are characters in
# string.punctuation for use in the function nopunc
spacestring = ''.join([" " for i in xrange(len(string.punctuation))])

# consumes a string s and returns the string with all punctuation characters
# replaced by spaces
def nopunc(s):
	return s.translate(string.maketrans(string.punctuation, spacestring))

def frequency(s):
	freq = {}
	for line in s.splitlines():
		for word in nopunc(line.strip().lower()).split():
			freq[word] = freq.get(word, 0) + 1
	return freq