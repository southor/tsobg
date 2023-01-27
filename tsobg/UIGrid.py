
class UIGrid():
	
	def __initCells(self):
		self.rows = []
		self.itemIndex = {}
		for i in range(0, self.nRows):
			row = [None]*self.nColumns
			self.rows.append(row)
			
	# returns ui position (pixelX, pixelY)
	def __getCellUIPos(self, rowN, colN):
		x = self.uiOffsetPos[0] + colN * self.uiCellSize[0]
		y = self.uiOffsetPos[1] + rowN * self.uiCellSize[1]
		return x,y
	
	# returns grid position (rowN, colN)
	def __findItem(self, item):
		for rowN,row in enumerate(self.rows):
			for colN,cell in enumerate(row):
				if cell == item:
					return rowN,colN
		return None

	def __findFreeCell(self):
		""" returns grid position as (colN, rowN) or None if no free cell was found """
		for rowN,row in enumerate(self.rows):
			for colN,cell in enumerate(row):
				if cell == None:
					return (colN,rowN)
		return None

	def __grow(self):
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
					nColumns: int,
					nRows: int,
					uiCellSize: tuple,
					**kwargs):
		self.uiCellSize = uiCellSize
		self.uiOffsetPos = kwargs.get("uiOffsetPos", (0, 0))
		self.nColumns = nColumns
		self.nRows = nRows
		self.nItems = 0
		self.minNColumns = nColumns
		self.minNRows = nRows
		self.maxNItems = kwargs.get("maxNItems", nColumns * nRows)
		self.autoGrow = kwargs.get("autoGrow", "rows")
		self.growFlag = kwargs.get("growFlag", False)
		#if self.nSpaces > nColumns * nRows:
		#	raise RuntimeError("nSpaces={} is too many for grid {}x{}.".format(self.nSpaces, nColumns, nRows))
		#if self.maxNColumns == None and self.maxNRows == None:
		#	raise RuntimeError("Must specify at least one of maxNColumns, maxNRows.")
		#if self.maxNColumns != None and self.maxNRows != None and self.nSpaces != None:
		#	raise RuntimeError("UIGrid constructor was called with 3 optional args (maxNColumns, maxNRows, nSpaces), only 2 of three can be used.")
		self.__initCells()
		
	#def getNSpaces(self):
	#	return self.nSpaces

	#def getNOccupied(self):
	#	return self.nOccupied

	#def getNUnoccupied(self):
	#	return self.nSpaces - self.nOccupied

	def getMaxNItems(self):
		return self.maxNItems

	def getNItems(self):
		return self.nItems

	#def getNFreeSpaces(self):
	#	""" Number of items that can be added before maxNItems is reached """
	#	return self.maxNItems - self.nItems

	def isFull(self):
		assert(self.nItems <= self.maxNItems)
		return self.nItems >= self.maxNItems

	def getCurrentUISize(self):
		""" Returns the current grid size """
		return (self.uiOffsetPos[0] + self.nColumns * self.uiCellSize[0], # width
				self.uiOffsetPos[1] + self.nRows * self.uiCellSize[1]) # height

	def growthHappened(self, clearFlag=False):
		res = self.growFlag
		if clearFlag:
			self.growFlag = False
		return res
	
	def addItem(self, item):
		""" 
		Puts the item in the first free available space.
		Triggers a growFlag=True if the occupied portion of grid has grown (new row or column)
		returns ui position of the cell that was taken.
		return None if no free space exists
		"""
		if self.isFull():
			return None
		gridPos = self.__findFreeCell()
		if not gridPos:
			self.__grow()
			gridPos = self.__findFreeCell()
		assert(gridPos)
		colN,rowN = gridPos
		assert(self.rows[rowN][colN] == None)
		self.rows[rowN][colN] = item
		self.nItems += 1
		return self.__getCellUIPos(rowN, colN)
	
	def removeItem(self, item):
		gridPos = self.__findItem(item)
		if gridPos:
			rowN,colN = gridPos
			self.rows[rowN][colN] = None
			self.nItems -= 1
		return bool(gridPos)
		
		
	"""	
	# add the items into the first free cells we find
	# returns the items that were not added (due to lack of free cells)
	def fillWithItems(self, items):
		if not isinstance(items, list):
			item = list(items)
		i = 0
		nItemsToAdd = len(items)
		for row in self.rows:
			for j,cell in enumerate(row):
				if i >= nItemsToAdd:
					break # all items were added already
				if cell == None:
					row[j] = items[i]
					i += 1
		# TODO: store into client gui update structure
		return items[i:]
	
	# returns item or None
	def getItem(self, row, column):
		return self.rows[row][column]
	
	def setItem(self, item, row, column):
		if self.rows[row][column] == None:
			self.nItems += 1
		if item == None:
			self.nItems -= 1
		self.rows[row][column] = item
		# TODO store into client gui update structure
	
	# sets that cell to None
	def removeItem(self, row, column):
		if self.rows[row][column] != None:
			self.nItems -= 1
			self.rows[row][column] = None
			# TODO store into client gui update structure
			
	# yields all cell items that are not None
	def allItems(self):
		for row in rows:
			for cell in row:
				if cell != None:
					yield cell
					
	# extracts all current uiChanges and resets the internal list
	def extractUIChanges(self):
		if self.uiChanges:
			res = self.uiChanges
			self.uiChanges = []
			return res
		else:
			return []
			
	"""