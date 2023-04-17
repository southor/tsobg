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

	def getObject(self):
		return grid.getItem(self)

	def getObject(self, colN, rowN):
		return self.grid.getItemAtCell(colN, rowN)

	def getObjectLayoutArgs(self, object, recursive=False):
		""" returns grid position as (colN, rowN) """
		return self.grid.getItemGridPos(object, recursive)

	def addObject(self, object):
		uiPos = self.grid.addItem(object)
		if not uiPos:
			return False
		object.setUIPos(uiPos)
		return True
	
	def addObject(self, object, colN, rowN):
		uiPos = self.grid.addItemAtCell(object, colN, rowN)
		if not uiPos:
			return False
		object.setUIPos(uiPos)
		return True

	def hasObject(self, object, recursive=False, remove=False):
		return self.grid.hasItem(object, recursive=recursive, remove=remove)
		#self.grid.visitItems(visitor)
