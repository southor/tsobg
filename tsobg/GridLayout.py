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

	def getNObjects(self):
		return self.grid.getNItems()

	def isFull(self):
		return self.grid.isFull()

	def hasObject(self, object):
		return self.grid.hasItem(object)

	def getObjectCoordinates(self, object):
		return self.grid.getItemGridPos(object)

	def getFirstObject(self, remove=False):
		return grid.getFirstItem(remove)

	def getObjectAt(self, colN, rowN):
		return self.grid.getItemAt(colN, rowN)

	def addObject(self, object):
		uiPos = self.grid.addItem(object)
		if not uiPos:
			return False
		object.setLayoutPos(uiPos)
		return True
	
	def addObjectAt(self, object, colN, rowN):
		uiPos = self.grid.addItemAt(object, colN, rowN)
		if not uiPos:
			return False
		object.setLayoutPos(uiPos)
		return True

	def removeObject(self, object):
		if self.grid.removeItem(object):
			return True
		return False

	def removeObjectAt(self, colN, rowN):
		""" returns the object that was removed, if any """
		return self.grid.removeItemAt(colN, rowN)

	def visitCellsReduce(self, visitFunc, initRes=None, visitOnlyOccupied=False):
		return self.grid.visitCellsReduce(visitFunc, initRes, visitOnlyOccupied=visitOnlyOccupied)

	def visitCellsShortcut(self, visitFunc, failRes=None, visitOnlyOccupied=False):
		return self.grid.visitCellsShortcut(visitFunc, failRes, visitOnlyOccupied=visitOnlyOccupied)

	def visitObjectsReduce(self, visitFunc, initRes=None):
		return self.grid.visitCellsReduce(visitFunc, initRes, visitOnlyOccupied=True)

	def visitObjectsShortcut(self, visitFunc, failRes=None):
		return self.grid.visitCellsShortcut(visitFunc, failRes, visitOnlyOccupied=True)

