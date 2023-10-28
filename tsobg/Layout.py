
class Layout():

	def getNRows(self):
		raise NotImplementedError("getNRows(self)")

	def getNColumns(self):
		raise NotImplementedError("getNColumns(self)")

	def getGridSize(self):
		raise NotImplementedError("getGridSize(self)")

	def getNObjects(self):
		raise NotImplementedError("getNObjects(self)")

	def isFull(self):
		raise NotImplementedError("isFull(self)")

	def hasObject(self, object):
		raise NotImplementedError("hasObject(self, object)")

	def getObjectPlace(self, object):
		raise NotImplementedError("getObjectPlace(self, object)")

	def getFirstObject(self, remove=False):
		raise NotImplementedError("getFirstObject(self, remove=False)")

	def getObjectAt(self, place):
		raise NotImplementedError("getObjectAt(self, place)")

	def getAllObjects(self):
		res = []
		self.visitObjectsReduce(lambda place,object,_: res.append(object))
		return res

	def getAllObjectsPlaceTuple(self):
		res = []
		self.visitObjectsReduce(lambda place,object,_: res.append((place, object)))
		return res

	def addObject(self, object):
		raise NotImplementedError("addObject(self, object)")

	def setObjectAt(self, place, object, allowReplace=True):
		"""
		Can be used to add or remove an object at a cell.
		If object is None:
			If cell contains an object:
				The object in the cell is removed.
				Returns (True,removedObject)
			If cell is empty:
				Returns (False,None)
		If object is non-None (then it must be of instance GameObject):
			If we have reached max number of objects (as set by maxNItems kwarg):
				Returns (False,None)
			Else If cell contains an object
				if allowReplace == True
					The object in the cell is replaced.
					Returns (True,removedObject)
				Else:
					Returns (False,blockingObject)
			If cell is empty:
				The object is added to the cell.
				Returns (True,None)
		"""
		raise NotImplementedError("setObjectAt(self, place, object)")

	def removeObject(self, object):
		raise NotImplementedError("removeObject(self, object)")

	def removeObjectAt(self, place):
		""" returns the removed object, or None if there was no object to remove """
		res,removedObj = self.setObjectAt(place, None)
		return removedObj

	def removeAllObjects(self, visitFunc=None):
		"""
		Calls visitFunc(place, object) for each removed object (if visitFunc is non-None)
		returns number of objects removed
		"""
		raise NotImplementedError("removeAllObjects(self)")
	
	def visitCellsReduce(self, visitFunc, initRes=None, visitOnlyOccupied=False):
		raise NotImplementedError("visitCellsReduce(self, visitFunc, initRes=None)")

	def visitCellsShortcut(self, visitFunc, failValue=None, visitOnlyOccupied=False):
		raise NotImplementedError("visitCellsShortcut(self, visitFunc, failValue=None)")

	def visitObjectsReduce(self, visitFunc, initRes=None):
		return self.visitCellsReduce(visitFunc, initRes, visitOnlyOccupied=True)

	def visitObjectsShortcut(self, visitFunc, failRes=None):
		return self.visitCellsShortcut(visitFunc, failRes, visitOnlyOccupied=True)
