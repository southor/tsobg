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

	def _updateSurfaceDivSize(self):
		surfaceSize = self.grid.getCurrentUISize()
		self.uiInterface.stageUIChange(("set_div", self.surfaceDivID, {"size": surfaceSize}))

	def __init__(self, uiInterface:UIInterface, surfaceDivID, gridSpaces:tuple, **kwargs):
		uiOffsetPos = kwargs.get("uiOffsetPos", (0, 0))
		uiOffsetPos = (uiOffsetPos[0] + CardGrid.cellPadding,
						uiOffsetPos[1] + CardGrid.cellPadding)
		self.uiInterface = uiInterface
		self.surfaceDivID = surfaceDivID
		cellSize = (cardSize[0] + CardGrid.cellPadding,
					cardSize[1] + CardGrid.cellPadding)
		maxNCards = kwargs.get("maxNCards", gridSpaces[0] * gridSpaces[1])
		self.grid = UIGrid(gridSpaces, cellSize, uiOffsetPos=uiOffsetPos, maxNItems=maxNCards, autoGrow="rows")
		self.autoCollapse = kwargs.get("autoCollapse", False)
		#surfaceSize = (uiOffsetPos[0] + gridSpaces[0] * cellSize[0], # width
		#				uiOffsetPos[1] + gridSpaces[1] * cellSize[1]) # height
		#surfaceSize = self.grid.getCurrentUISize()
		#uiInterface.stageUIChange(("set_div", surfaceDivID, {"size": surfaceSize}))
		self._updateSurfaceDivSize()

	def getNSpaces(self):
		return self.grid.getMaxNItems()

	def nCards(self):
		return self.grid.getNItems()

	def nFreeSpaces(self):
		return self.grid.getMaxNItems() - self.grid.getNItems()

	def collapse(self):
		movedCardsTuples = self.grid.collapse()
		for card,uiPos in movedCardsTuples:
			card.setDiv(self.uiInterface, pos=uiPos)

	def addCard(self, card:Card, extraDivOpts:dict = {}):
		""" 
		If a free cell is found then it puts the card there and sends the corresponding UI updates.
		returns True if completed, and False if no free cell exists.
		"""
		uiPos = self.grid.addItem(card)
		if uiPos:
			if self.grid.growthHappened(clearFlag=True):
				self._updateSurfaceDivSize()
			divOpts = {"parent":self.surfaceDivID, "pos":uiPos}
			divOpts.update(extraDivOpts)
			card.setDiv(self.uiInterface, **divOpts)
		return bool(uiPos)

	def removeCard(self, card:Card, extraDivOpts:dict = {}):
		if self.grid.removeItem(card):
			if self.autoCollapse:
				self.collapse()
			divOpts = {**{"parent":None}, **extraDivOpts}
			card.setDiv(self.uiInterface, **divOpts)
			return True
		else:
			return False
