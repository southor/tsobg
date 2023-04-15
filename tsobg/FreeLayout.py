
from .Layout import Layout

class FreeLayout(Layout):
	
	def __init__(self, limit=float('inf')):
		self.items = set()
		self.limit = limit

	def getNObjects(self):
		return len(self.items)

	def isFull(self):
		return len(self.items) >= self.limit

	def getObject(self):
		for item in self.items:
			return item
		return None

	def addObject(self, object):
		return self.addObject(self, object, (0,0))
	
	def addObject(self, object, uiPos="auto"):
		if self.isFull():
			return False
		self.items.add(object)
		object.setUIPos(uiPos)
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

