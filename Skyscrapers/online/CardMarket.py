import sys
from pathlib import Path

# import tsobg BaseGame
pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent.parent))
from tsobg import Deck
from tsobg import UIGrid
from tsobg import UIChangeInterface

# import SkyScrapers cards
sys.path.append(str(pathHere.parent))
from card_graphics import cardSize
from card_data import getAllCards


class CardMarket():

	nSpaces = 8
	cellPadding = 10
	
	def __init__(self, uiChangeInterface: UIChangeInterface):
		self.deck = Deck(getAllCards())
		cellSize = (cardSize[0] + CardMarket.cellPadding,
					cardSize[1] + CardMarket.cellPadding)
		self.grid = UIGrid(2, 4, cellSize, generateUIChanges = True)
	
	def nCards(self):
		return self.grid.getNItems()
	
	def fillUp(self):
		nMissingCards = CardMarket.nSpaces - self.nCards()
		newCards = self.deck.draw(nMissingCards)
		res = self.grid.fillWithItems(newCards)
		assert(res == [])
	
	