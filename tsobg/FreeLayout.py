
class FreeLayout():
	
	def __init__(self):
		self.items = set()

	def getNObjects(self):
		return len(self.items)

	def isFull(self):
		return False

	def getObject(self):
		for item in self.items:
			return item
		return None

	def addObject(self, object):
		return self.addObject(self, object, (0,0))
	
	def addObject(self, object, uiPos):
		self.items.add(object)
		object.setUIPos(uiPos)
		return True
	
	def removeObject(self, object):
		if object not in self.items:
			return False
		self.items.remove(object)
		return True

