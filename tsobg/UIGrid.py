
class UIGrid():
	
	def _initCells(self):
		self.rows = []
		self.itemIndex = {}
		for i in range(0, self.nRows):
			row = [None]*self.nColumns
			self.rows.append(row)

	#def _findAnyItem(self):
	#	""" returns first grid position that contains an object as (colN, rowN), None otherwise """
	#	for rowN,row in enumerate(self.rows):
	#		for colN,cell in enumerate(row):
	#			if cell:
	#				return colN,rowN
	#	return None
	
	#def _findItem(self, item):
	#	""" returns the grid position where item is located as (colN, rowN), None if not found """
	#	for rowN,row in enumerate(self.rows):
	#		for colN,cell in enumerate(row):
	#			if cell is item:
	#				return colN,rowN
	#	return None

	#def _findFreeCell(self):
	#	""" returns a free grid position as (colN, rowN) or None if no free cell was found """
	#	for rowN,row in enumerate(self.rows):
	#		for colN,cell in enumerate(row):
	#			if cell == None:
	#				return (colN,rowN)
	#	return None

	def _grow(self):
		if self.autoGrow == "columns":
			newRows = []
			for i,row in enumerate(self.rows):
				newRows.append(row + [None])
			self.rows = newRows
			self.nColumns += 1
		elif self.autoGrow == "rows":
			self.rows.append([None]*self.nColumns)
			self.nRows += 1
		else:
			raise RuntimeError("Invalid autoGrow values: " + str(self.autoGrow))
		self.growFlag = True
	
	def __init__(self,
					nColsRows: tuple,
					uiCellSize: tuple,
					**kwargs):
		self.uiCellSize = uiCellSize
		self.uiOffsetPos = kwargs.get("uiOffsetPos", (0, 0))
		self.nColumns = nColsRows[0]
		self.nRows = nColsRows[1]
		self.nItems = 0
		self.minNColumns = nColsRows[0]
		self.minNRows = nColsRows[1]
		self.maxNItems = kwargs.get("maxNItems", nColsRows[0] * nColsRows[1])
		self.autoGrow = kwargs.get("autoGrow", "rows")
		self.growFlag = kwargs.get("growFlag", False)
		self._initCells()

	def getMaxNItems(self):
		return self.maxNItems

	def getNItems(self):
		return self.nItems

	def getNRows(self):
		return self.nRows

	def getNColumns(self):
		return self.nColumns

	def isFull(self):
		assert(self.nItems <= self.maxNItems)
		return self.nItems >= self.maxNItems

	def getCurrentUISize(self):
		""" Returns the total UI size in pixels as (width, height) """
		return (self.uiOffsetPos[0] + self.nColumns * self.uiCellSize[0], # width
				self.uiOffsetPos[1] + self.nRows * self.uiCellSize[1]) # height

	def growthHappened(self, clearFlag=False):
		res = self.growFlag
		if clearFlag:
			self.growFlag = False
		return res

	# returns ui position (pixelX, pixelY)
	def getCellUIPos(self, colN, rowN):
		x = self.uiOffsetPos[0] + colN * self.uiCellSize[0]
		y = self.uiOffsetPos[1] + rowN * self.uiCellSize[1]
		return x,y

	def visitCellsReduce(self, visitFunc, initRes=None, visitOnlyOccupied=False):
		"""
		Visits all the cells in the grid and calls visitFunc(colN, rowN, cell, previousRes)
		previousRes contains the return value from the previous visitorFunc call.
		For the first cell the "previousRes" argument will be set to the value of the "initRes" argument.
		Returns the return value of the last visitFunc call.
		"""
		res = initRes
		for rowN,row in enumerate(self.rows):
				for colN,cell in enumerate(row):
					if cell != None or not visitOnlyOccupied:
						res = visitFunc(colN, rowN, cell, res)
		return res

	def visitCellsShortcut(self, visitFunc, failRes=None, visitOnlyOccupied=False):
		"""
		Visits all the cells in the grid and calls visitFunc(colN, rowN, cell)
		If the return value of a visitFunc call evaluates to True the iteration will stop and the value is returned.
		If all return values evaluates to False then failRes is returned.
		"""
		for rowN,row in enumerate(self.rows):
				for colN,cell in enumerate(row):
					if cell != None or not visitOnlyOccupied:
						res = visitFunc(colN, rowN, cell)
						if res:
							return res
		return failRes


	def hasItem(self, item):
		for rowN,row in enumerate(self.rows):
			if item in row:
				return True
		return False

	def getItemGridPos(self, item):
		def visitCell(colN, rowN, cell):
			return (colN, rowN) if cell is item else None
		return self.visitCellsShortcut(visitCell)

	#def getItemGridPos(self, item, recursive=False):
	#	""" 
	#	Returns the grid position where item is located as (colN, rowN), None if not found.
	#	If recursive is set to True it will search among children recursively for item (children must have method "hasObject").
	#	If the item is found recursively this way, the grid position for the child of this UIGrid that contained the item is returned.
	#	"""
	#	gridPos = self._findItem(item)
	#	if gridPos:
	#		return gridPos
	#	if recursive:
	#		for rowN,row in enumerate(self.rows):
	#			for colN,cell in enumerate(row):
	#				if cell:
	#					assert(cell is not item)
	#					if cell.hasObject(item, recursive=recursive):
	#						return colN,rowN
	#	return None


	def getFirstFreeGridPos(self):
		""" For the first ockupied cell found, return the grid position otherwise None """
		for rowN,row in enumerate(self.rows):
			for colN,cell in enumerate(row):
				if cell == None:
					return (colN,rowN)
		return None
	
	def getFirstItem(self, remove=False):
		""" For the first ockupied cell found, return the item there, otherwise None """
		res = self.visitCellsShortcut(lambda colN, rowN, cell: (colN, rowN, cell) if cell else None)
		if not res:
			return None
		colN,rowN,item = res
		if remove:
			removeItemAt(colN,rowN)
		return item

	def getItemAt(self, colN, rowN):
		return self.rows[rowN][colN]
	
	def addItem(self, item):
		""" 
		Puts the item in the first free available space.
		Triggers a growFlag=True if the occupied portion of grid has grown (new row or column)
		returns ui position of the cell that was taken.
		return None if no free space exists
		"""
		if self.isFull():
			return None
		gridPos = self.getFirstFreeGridPos()
		if not gridPos:
			self._grow()
			gridPos = self.getFirstFreeGridPos()
		assert(gridPos)
		colN,rowN = gridPos
		assert(self.rows[rowN][colN] == None)
		self.rows[rowN][colN] = item
		self.nItems += 1
		return self.getCellUIPos(colN,rowN)

	def addItemAt(self, item, colN, rowN):
		"""
		returns ui position of the cell.
		return None if the space was not free
		"""
		if self.isFull():
			return None
		if self.rows[rowN][colN]:
			return None
		self.rows[rowN][colN] = item
		return self.getCellUIPos(colN, rowN)

	#def hasItem(self, item, recursive=False, remove=False):
	#	gridPos = self._findItem(item)
	#	if gridPos:
	#		if remove:
	#			colN,rowN = gridPos
	#			self.rows[rowN][colN] = None
	#			self.nItems -= 1
	#		return True
	#	if recursive:
	#		for rowN,row in enumerate(self.rows):
	#			for colN,cell in enumerate(row):
	#				if cell:
	#					assert(cell is not item)
	#					if cell.hasObject(item, recursive=recursive, remove=remove):
	#						return True
	#	return False
	
	#def removeItem(self, item, recursive=False):
	#	return self.hasItem(item, recursive=recursive, remove=True)

	def removeItem(self, item):
		"""
		returns the grid position of the removed item as (colN, rowN), or None if item not found.
		"""
		gridPos = self.getItemGridPos(item)
		if gridPos:
			colN,rowN = gridPos
			self.rows[rowN][colN] = None
			self.nItems -= 1
			return colN,rowN
		return None

	def removeItemAt(self, colN, rowN):
		"""
		returns the item that was removed, None otherwise
		"""
		item = self.rows[rowN][colN]
		self.rows[rowN][colN] = None
		return item