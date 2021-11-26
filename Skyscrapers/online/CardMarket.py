import sys
from pathlib import Path

# import tsobg BaseGame
pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent.parent))
from tsobg import Deck
from tsobg import UIGrid
from tsobg import UIChangeInterface

# import SkyScraper cards
from Card import Card, createAllCards
pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent))
from card_graphics import cardSize


class CardMarket():

	nSpaces = 8
	cellPadding = 10
	
	def __initCardDict(self, allCards):
		self.cardDict = {}
		for card in allCards:
			self.cardDict[card.id] = card
	
	def __lookupCardId(self, cardId):
		return self.cardDict[cardId]
	
	def __init__(self, uiInterface: UIChangeInterface):
		self.uiInterface = uiInterface
		allCards = createAllCards()
		self.__initCardDict(allCards)
		self.deck = Deck(allCards)
		cellSize = (cardSize[0] + CardMarket.cellPadding,
					cardSize[1] + CardMarket.cellPadding)
		self.grid = UIGrid(2, 4, cellSize)
	
	def nCards(self):
		return self.grid.getNOccupied()
	
	def fillUp(self):
		nMissingCards = CardMarket.nSpaces - self.nCards()
		newCards = self.deck.draw(nMissingCards)
		for card in newCards:
			uiPos = self.grid.addItem(card)
			card.setDiv(self.uiInterface, parent="center", pos=uiPos)
	
	