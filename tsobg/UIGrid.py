
class UIGrid():
	
	def __initCells(self):
		self.rows = []
		for i in range(0, self.nRows):
			row = [None]*self.nColumns
			self.rows.append(row)
	
	def __init__(self,
					nColumns: int,
					nRows: int,
					cellSize: tuple,
					**kwargs):
		self.nColumns = nColumns
		self.nRows = nRows
		self.cellSize = cellSize
		self.nItems = 0 # nItems placed in the grid
		self.__initCells()
		if kwargs.get("generateUIChanges", False):
			self.uiChanges = []
		else:
			self.uiChanges = None
		
	def getNItems(self):
		return self.nItems
		
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