import sys
from pathlib import Path

pathHere = Path(__file__).absolute().parent

# tsobg imports
sys.path.append(str(pathHere.parent.parent))
from tsobg import UIGrid
from tsobg import UIChangeInterface

# Skyscrapers imports
sys.path.append(str(pathHere.parent))
from Card import Card
from card_graphics import cardSize



class CardGrid():
	
	cellPadding = 10

	def __init__(self, uiInterface: UIChangeInterface, surfaceDivID, gridSpaces: tuple, **kwargs):
		uiOffsetPos = kwargs.get("uiOffsetPos", (10, 10))
		self.uiInterface = uiInterface
		self.surfaceDivID = surfaceDivID
		cellSize = (cardSize[0] + CardGrid.cellPadding,
					cardSize[1] + CardGrid.cellPadding)
		self.grid = UIGrid(gridSpaces[0], gridSpaces[1], cellSize, uiOffsetPos=uiOffsetPos)

	def nCards(self):
		return self.grid.getNOccupied()

	def addCard(self, card: Card):
		uiPos = self.grid.addItem(card)
		card.setDiv(self.uiInterface, parent=self.surfaceDivID, pos=uiPos)
