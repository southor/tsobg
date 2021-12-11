import sys
from pathlib import Path

# tsobg imports
pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent.parent))
from tsobg import Deck
from tsobg import UIChangeInterface

# import SkyScraper cards
from Card import Card, createAllCards
from CardGrid import CardGrid


class CardMarket(CardGrid):

	nSpaces = 8
	
	def __initCardDict(self, allCards):
		self.cardDict = {}
		for card in allCards:
			self.cardDict[card.id] = card
	
	def __lookupCardId(self, cardId):
		return self.cardDict[cardId]
	
	def __init__(self, uiInterface: UIChangeInterface):
		super().__init__(uiInterface, "center", (2, 4))
		allCards = createAllCards()
		self.__initCardDict(allCards)
		self.deck = Deck(allCards)
	
	def fillUp(self):
		nMissingCards = CardMarket.nSpaces - self.nCards()
		newCards = self.deck.draw(nMissingCards)
		for card in newCards:
			self.addCard(card)
	
	