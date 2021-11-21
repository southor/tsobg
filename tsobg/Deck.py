import random


class Deck():
	
	def __init__(self, cards, shuffle = True):
		self.cards = cards
		self.discardedCards = []
		if shuffle:
			self.shuffle()
	
	def shuffle(self, includeDiscardPile = True):
		if includeDiscardPile:
			self.cards += self.discardedCards
			self.discardedCards = []
		random.shuffle(self.cards)
		
	def nCards(self, includeDiscardPile = True):
		n = len(self.cards)
		if includeDiscardPile:
			n += len(self.discardedCards)
		return n
		
	def discard(self, cards):
		self.discardedCards += cards
	
	def draw(self, nDraws):
		drawnCards = []
		if nDraws > len(self.cards):
			# draw remaining cards, then shuffle in the discard pile
			drawnCards += reversed(self.cards)
			self.cards = []
			nDraws -= len(self.cards)
			self.shuffle(True)
		if nDraws > len(self.cards):
			# draw only the rest of the deck
			nDraws = len(self.cards)
		drawnCards += reversed(self.cards[-nDraws:]) # draw from end of deck
		self.cards = self.cards[:-nDraws] # remove drawn cards from deck
		return drawnCards # return drawn cards