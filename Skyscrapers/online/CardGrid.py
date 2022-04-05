import sys
from pathlib import Path

pathHere = Path(__file__).absolute().parent

# tsobg imports
sys.path.append(str(pathHere.parent.parent))
from tsobg import UIGrid
from tsobg import UIInterface

# Skyscrapers imports
sys.path.append(str(pathHere.parent))
from Card import Card
from card_graphics import cardSize



class CardGrid():
	
	cellPadding = 10

	def __init__(self, uiInterface:UIInterface, surfaceDivID, gridSpaces:tuple, **kwargs):
		uiOffsetPos = kwargs.get("uiOffsetPos", (10, 10))
		self.uiInterface = uiInterface
		self.surfaceDivID = surfaceDivID
		cellSize = (cardSize[0] + CardGrid.cellPadding,
					cardSize[1] + CardGrid.cellPadding)
		self.grid = UIGrid(gridSpaces[0], gridSpaces[1], cellSize, uiOffsetPos=uiOffsetPos)
		surfaceSize = (gridSpaces[0] * cellSize[0] + CardGrid.cellPadding, # width
						gridSpaces[1] * cellSize[1] + CardGrid.cellPadding) # height
		uiInterface.stageUIChange(("set_div", surfaceDivID, {"size": surfaceSize}))

	def getNSpaces(self):
		return self.grid.getNSpaces()

	def nCards(self):
		return self.grid.getNOccupied()

	def addCard(self, card:Card, extraDivOpts:dict = {}):
		uiPos = self.grid.addItem(card)
		divOpts = {"parent":self.surfaceDivID, "pos":uiPos}
		divOpts.update(extraDivOpts)
		card.setDiv(self.uiInterface, **divOpts)

	def removeCard(self, card:Card, extraDivOpts:dict = {}):
		if self.grid.removeItem(card):
			divOpts = {**{"parent":None}, **extraDivOpts}
			card.setDiv(self.uiInterface, **divOpts)
			return True
		else:
			return False
