
from .Layout import Layout

class FreeLayout(Layout):
	
	def __init__(self, maxNItems=float('inf')):
		self.items = []
		self.nItems = 0
		self.maxNItems = maxNItems

	def __str__(self):
		res = [item.getDivID() if item else "None" for item in self.items]
		return "FreeLayout[{}]".format(", ".join(res))

	def getNRows(self):
		return None

	def getNColumns(self):
		return None

	def getGridSize(self):
		return None,None

	def getNObjects(self):
		assert(self.nItems >= 0 and self.nItems <= len(self.items))
		return self.nItems

	def isFull(self):
		return self.nItems >= self.maxNItems

	def verifyIndexType(value, methodName, paramName="index"):
		if not isinstance(value, int):
			raise TypeError("{} {} must be an integer, was {}".format(methodName, paramName, type(value)))

	def hasObject(self, object):
		return object in self.items
	
	def getObjectPlace(self, object):
		try:
			return self.items.index(object)
		except:
			return None

	def getFirstFreePlace(self, startIndex=0):
		FreeLayout.verifyIndexType(value, "getFirstFreePlace(self, startIndex)", "startIndex")
		try:
			return self.items(element).index(None)
		except:
			return None

	def getFirstTakenPlace(self, startIndex=0):
		FreeLayout.verifyIndexType(value, "getFirstTakenPlace(self, startIndex)", "startIndex")
		for i in range(startIndex, self.nItems):
			if self.items[i] != None:
				return i
		return None

	def getFirstObject(self, remove=False):
		idx = None
		res = None
		for i,item in enumerate(self.items):
			if item:
				idx = i
				res = item
				break
		if remove and idx != None:
			self.items[idx] = None
			self.nItems -= 1
		return res
		#if len(self.items) == 0:
		#	return None
		#item = self.items.pop()
		#if not remove:
		#	self.items.add(item)
		#return item

	def getObjectAt(self, index):
		FreeLayout.verifyIndexType(index, "getObjectAt(self, index)")
		try:
			return self.items[index]
		except:
			return None

	def addObject(self, object):
		if self.isFull():
			return False
		try:
			idx = self.items.index(None)
			self.items[idx] = object
		except:
			self.items.append(object)
		self.nItems += 1
		return True

	def setObjectAt(self, index, object, allowReplace=True):
		FreeLayout.verifyIndexType(index, "setObjectAt")
		nCells = len(self.items)
		isFull = self.isFull()
		# extend array if needed
		if index >= nCells:
			# index is beyond the allocated array
			if (not object) or isFull:
				return False,None
			# object is a GameObject that is allowed to be added
			# extend the array
			nNew = index + 1 - nCells
			self.items.extend([None * nNew])
		# get prevItem
		prevItem = self.items[index]
		# update nItems member
		if object:
			if prevItem:
				if not allowReplace:
					return False,prevItem
			else:
				if isFull:
					return False,None
				self.nItems += 1

		else:
			if not prevItem:
				return False,prevItem
			self.nItems -= 1
			assert(self.nItems >= 0)
		# write to the cell
		self.items[index] = object	
		return True,prevItem

	def removeObject(self, object):
		try:
			idx = self.items.index(object)
			assert(self.nItems >= 1)
			self.items[idx] = None
			self.nItems -= 1
			return True
		except:
			return False

	def removeAllObjects(self, visitFunc=None):
		nRemoved = 0
		removedRes = []
		for i,cell in enumerate(self.items):
			if not cell:
				continue
			self.items[i] = None
			nRemoved += 1
			if visitFunc:
				removedRes.append((i,cell))
		assert(nRemoved == self.nItems)
		self.nItems = 0
		if visitFunc:
			for i,object in removedRes:
				visitFunc(i, object)
		return nRemoved

	def swap(self, placeA, placeB):
		FreeLayout.verifyIndexType(placeA, "swap(self, placeA, placeB)", "placeA")
		FreeLayout.verifyIndexType(placeB, "swap(self, placeA, placeB)", "placeB")
		objectA = self.items[placeA]
		objectB = self.items[placeB]
		self.items[placeA] = objectB
		self.items[placeB] = objectA

	def collapse(self, startIndex=0):
		""" returns a list of objects that was moved """
		FreeLayout.verifyIndexType(startIndex, "collapse(self, startIndex)", "startIndex")
		res = []
		curFree = startIndex
		while True:
			curFree = self.getFirstFreePlace(curFree)
			curTaken = self.getFirstTakenPlace(curFree)
			if curFree and curTaken:
				self.swap(curFree, curTaken)
				res.append(self.getObjectAt(curFree))
			else:
				break
		return res

	def visitCellsReduce(self, visitFunc, initRes=None, **kwargs):
		startPlace = kwargs.get("startPlace", 0)
		visitOnlyOccupied = kwargs.get("visitOnlyOccupied", False)
		FreeLayout.verifyIndexType(startPlace, "FreeLayout visitCellsReduce", "startPlace")
		res = initRes
		for i,cell in enumerate(self.items, startPlace):
			if cell or not visitOnlyOccupied:
				res = visitFunc(i, cell, res)
		return res

	def visitCellsShortcut(self, visitFunc, failValue=None, **kwargs):
		startPlace = kwargs.get("startPlace", 0)
		visitOnlyOccupied = kwargs.get("visitOnlyOccupied", False)
		FreeLayout.verifyIndexType(startPlace, "FreeLayout visitCellsShortcut", "startPlace")
		for i in range(startPlace, self.nItems):
			cell = self.items[i]
			if cell or not visitOnlyOccupied:
				res = visitFunc(i, cell)
				if res != None:
					return res
		return failValue
