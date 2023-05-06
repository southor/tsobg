
class Layout():


	def getNObjects(self):
		raise NotImplementedError("getNObjects(self)")

	def isFull(self):
		raise NotImplementedError("isFull(self)")

	def hasObject(self, object):
		raise NotImplementedError("hasObject(self, object)")

	def getObjectCoordinates(self, object):
		raise NotImplementedError("getObjectCoordinates(self, object)")

	def getFirstObject(self, remove=False):
		raise NotImplementedError("getFirstObject(self, remove=False)")

	def getObjectAt(self, colN, rowN):
		raise NotImplementedError("getObjectAt(self, colN, rowN)")

	def addObject(self, object):
		raise NotImplementedError("addObject(self, object)")

	def addObjectAt(self, object, colN, rowN):
		raise NotImplementedError("addObjectAt(self, object, pos)")

	def removeObject(self, object):
		raise NotImplementedError("removeObject(self, object)")

	def removeObjectAt(self, object, colN, rowN):
		raise NotImplementedError("removeObjectAt(self, object, colN, rowN)")
	
	def visitCellsReduce(self, visitFunc, initRes=None, visitOnlyOccupied=False):
		raise NotImplementedError("visitCellsReduce(self, visitFunc, initRes=None)")

	def visitCellsShortcut(self, visitFunc, failValue=None, visitOnlyOccupied=False):
		raise NotImplementedError("visitCellsShortcut(self, visitFunc, failValue=None)")

	def visitObjectsReduce(self, visitFunc, initRes=None):
		raise NotImplementedError("visitObjectsReduce(self, visitFunc, initRes=None)")

	def visitObjectsShortcut(self, visitFunc, failValue=None):
		raise NotImplementedError("visitObjectsShortcut(self, visitFunc, failValue=None)")
