import random


class Deck():
	
	def __init__(self, cards, autoShuffle = True):
		random.seed(42) # using fixed seed for now (required for game revert to produce the same deck shuffle)
		self.cards = cards.copy()
		self.discardedCards = []
		self.autoShuffle = autoShuffle
		if autoShuffle:
			self.shuffle(True)
	
	def shuffle(self, includeDiscardPile):
		if includeDiscardPile:
			self.cards += self.discardedCards
			self.discardedCards = []
		random.shuffle(self.cards)
		
	def nCards(self):
		n = len(self.cards)
		if self.autoShuffle:
			n += len(self.discardedCards)
		return n
		
	def discard(self, cards):
		self.discardedCards += cards
	
	def draw(self, nDraws):
		drawnCards = []
		if nDraws > len(self.cards):
			# draw remaining cards, then shuffle in the discard pile if autoShuffle is on
			nDraws -= len(self.cards)
			drawnCards += reversed(self.cards)
			self.cards = []
			if self.autoShuffle:
				self.shuffle(True)
		if nDraws > len(self.cards):
			# draw only the rest of the deck
			nDraws = len(self.cards)
		if nDraws > 0: 
			drawnCards += reversed(self.cards[-nDraws:]) # draw from end of deck
			self.cards = self.cards[:-nDraws] # remove drawn cards from deck
		return drawnCards # return drawn cards