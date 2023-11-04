
""" Stores items (of any type except None) in a custom grid """
class UIGrid():

	maxNColumns = 100
	maxNRows = 100
	
	def _initCells(self):
		self.rows = []
		self.itemIndex = {}
		for i in range(0, self.nRows):
			row = [None]*self.nColumns
			self.rows.append(row)

	def _grow(self):
		if self.autoGrow == None:
			return False
		if self.autoGrow == "columns" or self.autoGrow == "columns_first":
			if self.nColumns >= UIGrid.maxNColumns:
				raise RuntimeError(f"Cannot grow UIGrid further, already at {UIGrid.maxNColumns} columns.")
			#newRows = []
			#for i,row in enumerate(self.rows):
			#	newRows.append(row + [None])
			#self.rows = newRows
			#self.nColumns += 1
			if self.nRows == 0:
				self.nColumns += 1
			else:
				return self._growTo((self.nColumns, 0))
		elif self.autoGrow == "rows" or self.autoGrow == "rows_first":
			if self.nRows >= UIGrid.maxNRows:
				raise RuntimeError(f"Cannot grow UIGrid further, already at {UIGrid.maxNRows} rows.")
			self.rows.append([None]*self.nColumns)
			self.nRows += 1
		else:
			raise ValueError("Invalid autoGrow type: " + str(self.autoGrow))
		self.growFlag = True
		return True

	def _growTo(self, gridPos):
		if self.autoGrow == None:
			return False
		
		colN,rowN = gridPos
		assert(colN >= 0 and rowN >= 0)
		
		if colN >= self.nColumns:
			if self.autoGrow in ("columns", "columns_first", "rows_first"):
				if self.nColumns >= UIGrid.maxNColumns:
					raise RuntimeError(f"Cannot grow UIGrid further, already at {UIGrid.maxNColumns} columns.")
			else:
				return False

		if rowN >= self.nRows:
			if self.autoGrow in ("rows", "columns_first", "rows_first"):
				if self.nRows >= UIGrid.maxNRows:
					raise RuntimeError(f"Cannot grow UIGrid further, already at {UIGrid.maxNRows} rows.")
			else:
				return False

		if colN >= self.nColumns:
			nToAdd = colN + 1 - self.nColumns
			newRows = []
			for i,row in enumerate(self.rows):
				newRows.append(row + [None] * nToAdd)
			self.rows = newRows
			self.nColumns += nToAdd
		if rowN >= self.nRows:
			nToAdd = rowN + 1 - self.nRows
			for i in range(nToAdd):
				self.rows.append([None] * self.nColumns)
			self.nRows += nToAdd
		
		self.growFlag = True
		return True
	
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
		#self.autoGrow = kwargs.get("autoGrow", "rows")
		self.autoGrow = kwargs.get("autoGrow", None)
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

	def getSize(self):
		return (self.nColumns, self.nRows)

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
	def getCellUIPos(self, gridPos):
		x = self.uiOffsetPos[0] + gridPos[0] * self.uiCellSize[0]
		y = self.uiOffsetPos[1] + gridPos[1] * self.uiCellSize[1]
		return x,y

	def visitCellsReduce(self, visitFunc, initRes=None, visitOnlyOccupied=False):
		"""
		Visits all the cells in the grid and calls visitFunc((colN,rowN), cell, previousRes)
		previousRes contains the return value from the previous visitorFunc call.
		For the first cell the "previousRes" argument will be set to the value of the "initRes" argument.
		Returns the return value of the last visitFunc call.
		"""
		res = initRes
		for rowN,row in enumerate(self.rows):
				for colN,cell in enumerate(row):
					if cell != None or not visitOnlyOccupied:
						res = visitFunc((colN,rowN), cell, res)
		return res

	def visitCellsShortcut(self, visitFunc, failRes=None, visitOnlyOccupied=False):
		"""
		Visits all the cells in the grid and calls visitFunc((colN,rowN), cell)
		If the return value of a visitFunc call evaluates to True the iteration will stop and the value is returned.
		If all return values evaluates to False then failRes is returned.
		"""
		for rowN,row in enumerate(self.rows):
				for colN,cell in enumerate(row):
					if cell != None or not visitOnlyOccupied:
						res = visitFunc((colN,rowN), cell)
						if res:
							return res
		return failRes


	def hasItem(self, item):
		for rowN,row in enumerate(self.rows):
			if item in row:
				return True
		return False

	def getItemGridPos(self, item):
		def visitCell(gridPos, cell):
			return gridPos if cell is item else None
		return self.visitCellsShortcut(visitCell)

	def getFirstFreeGridPos(self):
		""" For the first ockupied cell found, return the grid position otherwise None """
		for rowN,row in enumerate(self.rows):
			for colN,cell in enumerate(row):
				if cell == None:
					return (colN,rowN)
		return None
	
	def getFirstItem(self, remove=False):
		""" For the first ockupied cell found, return the item there, otherwise None """
		res = self.visitCellsShortcut(lambda gridPos, cell: (gridPos, cell) if cell else None)
		if not res:
			return None
		gridPos,item = res
		if remove:
			removeItemAt(gridPos)
		return item

	def getItemAt(self, gridPos):
		colN,rowN = gridPos
		return self.rows[rowN][colN]
	
	def addItem(self, item):
		""" 
		Puts the item in the first free available space.
		Triggers a growFlag=True if the occupied portion of grid has grown (new row or column)
		returns ui position of the cell that was taken.
		return None if no free space exists
		"""
		if item == None:
			raise ValueError("Item to add must not be None, item=" + str(item))
		if self.isFull():
			return None
		gridPos = self.getFirstFreeGridPos()
		if not gridPos:
			if not self._grow():
				return None
			gridPos = self.getFirstFreeGridPos()
		assert(gridPos)
		colN,rowN = gridPos
		assert(self.rows[rowN][colN] == None)
		self.rows[rowN][colN] = item
		self.nItems += 1
		return self.getCellUIPos(gridPos)

	def addItemAt(self, pos, item):
		if item == None:
			raise ValueError("Item to add must not be None, item=" + str(item))
		uiPos,prevItem = self.setItemAt(pos, item, allowReplace=False)
		assert(prevItem == None)
		return uiPos

	def setItemAt(self, gridPos, item, allowReplace=True):
		"""
		Can be used to add or remove an item at a cell.
		If item is None:
			If cell contains an item:
				The item in the cell is removed.
				Returns (uiPos,removedItem)
			If cell is empty:
				Returns (uiPos,None)
		If item is non-None (Can be of any type expect None):
			If we have reached max number of items (as set by maxNItems kwarg):
				Returns (None,None)
			Else If cell contains an item:
				If allowReplace == True
					The item is replaced.
					Returns (uiPos,removedItem)
				Else
					Returns (None,blockingItem)
			If cell is empty:
				The item is added to the cell.
				Returns (uiPos,None)
		"""
		colN,rowN = gridPos

		if colN < 0 or rowN < 0:
			raise ValueError("Invalid gridPos (negative value): " + gridPos)
		if colN >= self.nColumns or rowN >= self.nRows:
			if not self._growTo(gridPos):
				raise ValueError("gridPos ({}) outside current limits ({})".format(gridPos, (self.nColumns, self.nRows)))
		uiPos = self.getCellUIPos(gridPos)
		#row = self.rows[rowN]
		prevItem = self.rows[rowN][colN]
		if item == None:
			if prevItem == None:
				return None,None
			else:
				self.nItems -= 1
		else:
			if prevItem == None:
				if self.isFull():
					return None,None
				self.nItems += 1
			elif not allowReplace:
				return None,prevItem
		self.rows[rowN][colN] = item
		return self.getCellUIPos(gridPos),prevItem

	def removeItem(self, item):
		"""
		returns the grid position of the removed item as (colN, rowN), or None if item not found.
		"""
		gridPos = self.getItemGridPos(item)
		if gridPos:
			colN,rowN = gridPos
			self.rows[rowN][colN] = None
			self.nItems -= 1
		return gridPos

	def removeItemAt(self, gridPos):
		"""
		returns the item that was removed, None otherwise
		"""
		colN,rowN = gridPos
		item = self.rows[rowN][colN]
		if item:
			self.rows[rowN][colN] = None
			self.nItems -= 1
		return item

	def removeAllItems(self, visitFunc=None):
		"""
		Calls visitFunc((colN,rowN), item) for each removed object (if visitFunc is non-None)
		returns number of items removed
		"""
		def removerFunc(gridPos, item, res):
			colN,rowN = gridPos
			row = self.rows[rowN]
			if row[colN] != None:
				res.append((gridPos, row[colN]))
				row[colN] = None
			return res
		removedRes = self.visitCellsReduce(removerFunc, [], visitOnlyOccupied=True)
		assert(len(removedRes) == self.nItems)
		self.nItems = 0
		if visitFunc:
			for pos,item in removedRes:
				visitFunc(pos, item)
		return len(removedRes)