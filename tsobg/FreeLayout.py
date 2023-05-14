
from .Layout import Layout

class FreeLayout(Layout):
	
	def __init__(self, maxNItems=float('inf')):
		self.items = set()
		self.maxNItems = maxNItems

	def getNRows(self):
		return None

	def getNColumns(self):
		return None

	def getGridSize(self):
		return None,None

	def getNObjects(self):
		return len(self.items)

	def isFull(self):
		return len(self.items) >= self.maxNItems

	def hasObject(self, object):
		return object in self.items
	
	def getObjectCoordinates(self, object):
		return None

	def getFirstObject(self, remove=False):
		if len(self.items) == 0:
			return None
		item = self.items.pop()
		if not remove:
			self.items.add(item)
		return item

	def getObjectAt(self, colN, rowN):
		if not (colN == None and rowN == None):
			raise ValueError("Passed incorrect arguments to FreeLayout.getObjectAt. arguments = {}, {}" + str(colN) + str(rowN))
		return self.getFirstObject()

	def addObject(self, object):
		if self.isFull():
			return False
		self.items.add(object)
		return True

	def removeObject(self, object):
		if object in self.items:
			self.items.remove(object)
			return True
		return False

	def removeAllObjects(self):
		""" returns number of objects removed """
		res = len(self.items)
		self.items.clear()
		return res

	def visitObjectsReduce(self, visitFunc, initRes=None):
		res = initRes
		for object in self.items:
			res = visitFunc(None, None, object, res)
		return res

	def visitObjectsShortcut(self, visitFunc, failValue=None):
		for object in self.items:
			res = visitFunc(None, None, object)
			if res:
				return res
		return failValue
