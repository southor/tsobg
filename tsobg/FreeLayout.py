
from .Layout import Layout

class FreeLayout(Layout):
	
	def __init__(self, maxNItems=float('inf')):
		self.items = []
		self.nItems = 0
		self.maxNItems = maxNItems

	def getNRows(self):
		return None

	def getNColumns(self):
		return None

	def getGridSize(self):
		return None,None

	def getNObjects(self):
		#return len(self.items)
		#nObjects = 0
		#for item in items:
		#return sum(x is not None for x in lst)
		assert(self.nItems >= 0 and self.nItems <= len(self.items))
		return self.nItems

	def isFull(self):
		return self.nItems >= self.maxNItems

	def hasObject(self, object):
		return object in self.items
	
	def getObjectCoordinates(self, object):
		try:
			return self.items.index(object)
		except:
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
		#if not (colN == None and rowN == None):
		#	raise ValueError("Passed incorrect arguments to FreeLayout.getObjectAt. arguments = {}, {}" + str(colN) + str(rowN))
		#return self.getFirstObject()
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
		#object.setLayoutPos(("auto", "auto"))
		return True
		#self.items.append(object)
		#self.nItems += 1
		#return True


	def setObjectAt(self, pos, object):
		n = len(self.items)
		isFull = self.isFull()

		if pos >= n:
			if isFull or not object:
				return False
			# object is a GameObject that is allowed to be added but we need to extend the array
			nNew = pos + 1 - n
			self.items.extend([None * nNew])

		if object:
			if isFull:
				return False
			if not self.items[pos]:
				self.nItems += 1
			else:
				return False
			#object.setLayoutPos(("auto", "auto"))
		else:
			if not self.items[pos]:
				return False
			self.nItems -= 1
		self.items[pos] = object	
		return True

	def removeObject(self, object):
		try:
			idx = self.items.index(object)
			assert(self.nItems >= 1)
			self.items[idx] = None
			self.nItems -= 1
			return True
		except:
			return False
		#if object in self.items:
		#	self.items.remove(object)
		#	self.nItems -= 1
		#	return True
		#return False

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

	def visitCellsReduce(self, visitFunc, initRes=None, visitOnlyOccupied=False):
		res = initRes
		for i,cell in enumerate(self.items):
			if cell or not visitOnlyOccupied:
				res = visitFunc(i, cell, res)
		return res

	def visitCellsShortcut(self, visitFunc, failValue=None, visitOnlyOccupied=False):
		for i,cell in enumerate(self.items):
			if cell or not visitOnlyOccupied:
				res = visitFunc(i, cell)
				if res:
					return res
		return failValue
