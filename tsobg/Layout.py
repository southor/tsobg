
class Layout():
	
	def _sumUICoords(*args):
		res = "auto"
		for arg in args:
			if arg != "auto":
				if res == "auto":
					res = arg
				else:
					res += arg
		return res

	def _getEffectiveUIPos(self, uiPos = ("auto", "auto")):
		return (Layout._sumUICoords(uiPos[0], self.padding[0]),
				Layout._sumUICoords(uiPos[1], self.padding[1]))
	
	def checkPadding(padding):
		if (type(padding) not in (list, tuple)) or (len(padding) != 2):
			raise ValueError("padding should be a list or tuple with 2 number members")
	
	def __init__(self, **kwargs):
		self.padding = kwargs.get("padding", ("auto", "auto"))
		Layout.checkPadding(self.padding)
	
	def getPadding():
		return self.padding

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

	def getFirstFreePlace(self, startPlace=None):
		""" For the first unoccupied cell found return the place, otherwise None """
		raise NotImplementedError("getFirstFreePlace(self, startPlace)")

	def getFirstTakenPlace(self, startPlace=None):
		""" For the first unoccupied cell found return the place, otherwise None """
		raise NotImplementedError("getFirstTakenPlace(self, startPlace)")

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

	def swap(self, placeA, placeB):
		raise NotImplementedError("swap(self, placeA, placeB)")

	def collapse(self, startPlace=None):
		raise NotImplementedError("collapse(self, startPlace)")
	
	def visitCellsReduce(self, visitFunc, initRes=None, **kwargs):
		""" 
		Visits all the cells and calls visitFunc(place, cell, previousRes)
		previousRes contains the return value from the previous visitorFunc call.
		For the first cell the "previousRes" argument will be set to the value of the "initRes" argument.
		Returns the return value of the last visitFunc call.
		kwargs: "startPlace" default value is first Cell, visitOnlyOccupied=False
		"""
		raise NotImplementedError("visitCellsReduce(self, visitFunc, initRes=None)")

	def visitCellsShortcut(self, visitFunc, failRes=None, **kwargs):
		"""
		Visits all the cells and calls visitFunc(place, cell)
		If the return value of one of the visitFunc calls is not None the iteration will stop and the value is returned.
		Note that any value other than None will stop iteration, including other falsy values.
		If all return values are None then all cells will be visited and failRes is returned.
		kwargs: "startPlace" default value is first Cell, visitOnlyOccupied=False
		"""
		raise NotImplementedError("visitCellsShortcut(self, visitFunc, failValue=None)")

	def visitObjectsReduce(self, visitFunc, initRes=None):
		return self.visitCellsReduce(visitFunc, initRes, visitOnlyOccupied=True)

	def visitObjectsShortcut(self, visitFunc, failRes=None):
		return self.visitCellsShortcut(visitFunc, failRes, visitOnlyOccupied=True)
