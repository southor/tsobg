from .Layout import Layout
from .UIGrid import UIGrid

class GridLayout(Layout):
	
	
	def _setMemberLayoutPos(self, object, uiPos):
		object.setLayoutPos(self._getEffectiveUIPos(uiPos))
	
	def __init__(self,
					nColsRows: tuple,
					uiCellSize: tuple,
					**kwargs):
		super().__init__(**kwargs)
		self.grid = UIGrid(nColsRows, uiCellSize, **kwargs)

	def __str__(self):
		return self.grid.toStr(lambda obj: obj.getDivID())

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

	def getObjectPlace(self, object):
		return self.grid.getItemGridPos(object)

	def getFirstFreePlace(self, startGridPos=(0,0)):
		return self.grid.getFirstFreeGridPos(startGridPos)

	def getFirstTakenPlace(self, startGridPos=(0,0)):
		return self.grid.getFirstTakenGridPos(startGridPos)

	def getFirstObject(self, remove=False):
		return self.grid.getFirstItem(remove)

	def getObjectAt(self, gridPos):
		return self.grid.getItemAt(gridPos)

	def addObject(self, object):
		uiPos = self.grid.addItem(object)
		if not uiPos:
			return False
		self._setMemberLayoutPos(object, uiPos)
		return True
	
	def setObjectAt(self, gridPos, object, allowReplace=True):
		#prevObject = self.grid.getItemAt(gridPos)
		uiPos,prevObject = self.grid.setItemAt(gridPos, object, allowReplace)
		if not uiPos:
			return False,prevObject
		if prevObject:
			prevObject.setLayoutPos(("auto", "auto"))
		if object:
			self._setMemberLayoutPos(object, uiPos)
		return True,prevObject

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
		def layoutPosResetter(place, obj):
			obj.setLayoutPos(("auto", "auto"))
			if visitFunc:
				visitFunc(place, obj)
		return self.grid.removeAllItems(visitFunc=layoutPosResetter)

	def swap(self, placeA, placeB):
		res = self.grid.swap(placeA, placeB)
		for object,uiPos in res:
			self._setMemberLayoutPos(object, uiPos)

	def collapse(self, startGridPos=(0, 0)):
		""" returns a list of objects that was moved """
		movedObjectsTuples = self.grid.collapse(startGridPos)
		res = []
		for object,uiPos in movedObjectsTuples:
			self._setMemberLayoutPos(object, uiPos)
			res.append(object)
		return res

	def visitCellsReduce(self, visitFunc, initRes=None, **kwargs):
		return self.grid.visitCellsReduce(visitFunc, initRes, **kwargs)

	def visitCellsShortcut(self, visitFunc, failRes=None, **kwargs):
		return self.grid.visitCellsShortcut(visitFunc, failRes, **kwargs)

