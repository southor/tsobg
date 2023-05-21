from .Layout import Layout
from .UIGrid import UIGrid

class GridLayout(Layout):
	
	def __init__(self,
					nColsRows: tuple,
					uiCellSize: tuple,
					**kwargs):
		self.grid = UIGrid(nColsRows, uiCellSize, **kwargs)

	def getNRows(self):
		return self.grid.getNRows()

	def getNColumns(self):
		return self.grid.getNColumns()

	def getGridSize(self):
		return self.grid.getSize()

	def getNObjects(self):
		return self.grid.getNItems()

	def isFull(self):
		return self.grid.isFull()

	def hasObject(self, object):
		return self.grid.hasItem(object)

	def getObjectCoordinates(self, object):
		return self.grid.getItemGridPos(object)

	def getFirstObject(self, remove=False):
		return self.grid.getFirstItem(remove)

	def getObjectAt(self, gridPos):
		return self.grid.getItemAt(gridPos)

	def addObject(self, object):
		uiPos = self.grid.addItem(object)
		if not uiPos:
			return False
		object.setLayoutPos(uiPos)
		return True
	
	def setObjectAt(self, gridPos, object):
		prevObject = self.grid.getItemAt(gridPos)
		uiPos = self.grid.setItemAt(gridPos, object)
		if not uiPos:
			return False
		if prevObject:
			prevObject.setLayoutPos(("auto", "auto"))
		if object:
			object.setLayoutPos(uiPos)
		return True

	def removeObject(self, object):
		if self.grid.removeItem(object):
			object.setLayoutPos(("auto", "auto"))
			return True
		return False

	def removeObjectAt(self, gridPos):
		""" returns the object that was removed, otherwise None """
		obj = self.grid.removeItemAt(gridPos)
		if obj:
			obj.setLayoutPos(("auto", "auto"))
		return obj

	def removeAllObjects(self, visitFunc=None):
		def layoutPosResetter(pos, obj):
			obj.setLayoutPos(("auto", "auto"))
			if visitFunc:
				visitFunc(pos, obj)
		return self.grid.removeAllItems(visitFunc=layoutPosResetter)

	def visitCellsReduce(self, visitFunc, initRes=None, visitOnlyOccupied=False):
		return self.grid.visitCellsReduce(visitFunc, initRes, visitOnlyOccupied=visitOnlyOccupied)

	def visitCellsShortcut(self, visitFunc, failRes=None, visitOnlyOccupied=False):
		return self.grid.visitCellsShortcut(visitFunc, failRes, visitOnlyOccupied=visitOnlyOccupied)

