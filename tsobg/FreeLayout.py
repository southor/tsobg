
from .Layout import Layout

class FreeLayout(Layout):
	
	def __init__(self, maxNItems=float('inf')):
		self.items = set()
		self.maxNItems = maxNItems

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
		#item = None
		#for itm in self.items:
		#	item = itm
		#	break
		#if remove and item:
		#	self.items.remove(item)
		#return item

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

	#def visitCellsReduce(self, visitFunc, initRes=None):
	#	return self.visitObjectsReduce(lambda object,res: visitFunc(None, None, object, res), initRes)

	#def visitCellsShortcut(self, visitFunc, failValue=None):
	#	return self.visitObjectsShortcut(lambda object: visitFunc(None, None, object), failValue)

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
