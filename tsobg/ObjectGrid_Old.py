
import sys
from pathlib import Path

import UIGrid
import UIInterface


class ObjectGrid():
	
	def __updateSurfaceDivSize(self):
		surfaceSize = self.grid.getCurrentUISize()
		self.uiInterface.stageUIChange(("set_div", self.surfaceDivID, {"size": surfaceSize}))

	def __init__(self, uiInterface:UIInterface, surfaceDivID, gridSpaces:tuple, cellSize:tuple, **kwargs):
		self.uiInterface = uiInterface
		self.surfaceDivID = surfaceDivID
		uiOffsetPos = kwargs.get("uiOffsetPos", (0, 0))
		maxNObjects = kwargs.get("maxNObjects", gridSpaces[0] * gridSpaces[1])
		self.grid = UIGrid(gridSpaces, cellSize, uiOffsetPos=uiOffsetPos, maxNItems=maxNObjects)
		self.__updateSurfaceDivSize()

	def getNSpaces(self):
		return self.grid.getMaxNItems()

	def nObjects(self):
		return self.grid.getNItems()

	def nFreeSpaces(self):
		return self.grid.getMaxNItems() - self.grid.getNItems()

	def addToFreeCell(self, obj:GameObject):
		"""
		If a free cell is found then it puts the object there and sends the corresponding UI updates.
		returns True if completed, and False if no free cell exists.
		"""
		uiPos = self.grid.addItem(obj)
		if uiPos:
			if self.grid.growthHappened(clearFlag=True):
				self.__updateSurfaceDivSize()
			obj.setParent(self.surfaceDivID)
			obj.setUIPos(uiPos)
		return bool(uiPos)

	def removeObject(self, obj:GameObject):
		if self.grid.removeItem(obj):
			obj.setParent(None)
			return True
		else:
			return False

	def getAtCell(self, rowN, colN):
		return self.grid.getItemAtCell(rowN, colN)

	def setAtCell(self, rowN, colN, item):
		return self.grid.setItemAtCell(rowN, colN, item)