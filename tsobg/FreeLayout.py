
from .Layout import Layout

class FreeLayout(Layout):
	
	def __init__(self, maxNItems=float('inf')):
		self.items = set()
		self.maxNItems = maxNItems

	def getNObjects(self):
		return len(self.items)

	def isFull(self):
		return len(self.items) >= self.maxNItems

	def getObject(self):
		for item in self.items:
			return item
		return None

	def getObjectLayoutArgs(self, object, recursive=False):
		if object in self.items:
			return object.getPos()
		if recursive:
			for item in self.items:
				if item.hasObject(object, recursive):
					return item.getPos()
		return None

	def addObject(self, object):
		return self.addObject(self, object, (0,0))
	
	def addObject(self, object, pos="auto"):
		if self.isFull():
			return False
		self.items.add(object)
		object.setPos(pos)
		return True

	def hasObject(self, object, recursive=False, remove=False):
		if object in self.items:
			if remove:
				self.items.remove(object)
			return True
		if recursive:
			for item in self.items:
				if item.hasObject(object, recursive, remove):
					return True
		return False

