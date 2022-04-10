
class UIGrid():
	
	def __initCells(self):
		self.rows = []
		self.itemIndex = {}
		self.nOccupied = 0 # nItems placed in the grid
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
	
	def __init__(self,
					nColumns: int,
					nRows: int,
					uiCellSize: tuple,
					**kwargs):
		self.nColumns = nColumns
		self.nRows = nRows
		self.uiCellSize = uiCellSize
		self.uiOffsetPos = kwargs.get("uiOffsetPos", (0, 0))
		self.__initCells()
		
	def getNSpaces(self):
		return self.nRows * self.nColumns

	def getNOccupied(self):
		return self.nOccupied

	def getNUnoccupied(self):
		return self.getNSpaces() - self.nOccupied
	
	def addItem(self, item):
		""" 
		puts the item in the first free cell
		returns ui position of cell that was taken
		return None if no free cell exists
		"""
		for rowN,row in enumerate(self.rows):
			for colN,cell in enumerate(row):
				if cell == None:
					row[colN] = item
					self.nOccupied += 1
					return self.__getCellUIPos(rowN, colN)
		return None
	
	def removeItem(self, item):
		gridPos = self.__findItem(item)
		if gridPos:
			rowN,colN = gridPos
			self.rows[rowN][colN] = None
			self.nOccupied -= 1
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