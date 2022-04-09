import random as orig_random

import sys


def seed(a=None):
	if a == None:
		seed = orig_random.randrange(sys.maxsize)
		a = orig_random.Random(seed)
	globals()["randSeed"] = a
	orig_random.seed(a)

def reset():
	""" resets the seed back to the last seed value """
	orig_random.seed(globals()["randSeed"])

def random():
	return orig_random.random()

def shuffle(x, randFunc=orig_random.random):
	"""
	Shuffle the sequence x in place.
	The optional argument randFunc is a 0-argument function returning a random float in [0.0, 1.0); by default, this is the function random().
	"""
	return orig_random.shuffle(x, randFunc)

def choice(seq):
	return orig_random.choice(seq)

