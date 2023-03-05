from .UIGrid import UIGrid

class GridLayout():
	
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

	def getObject(self):
		return grid.getItem(self)

	def getObject(self, rowN, colN):
		return grid.getItemAtCell(self, rowN, colN)

	def addObject(self, object):
		uiPos = grid.addItem(self, object)
		if not uiPos:
			return False
		object.setUIPos(uiPos)
		return True
	
	def addObject(self, object, rowN, colN):
		uiPos = self.grid.addItemAtCell(object, rowN, colN)
		if not uiPos:
			return False
		object.setUIPos(uiPos)
		return True
	
	def removeObject(self, object):
		return self.grid.removeItem(object)
