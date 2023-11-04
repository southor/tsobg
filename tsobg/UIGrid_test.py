import unittest

if __name__ == '__main__':
	from UIGrid import UIGrid
else:
	from .UIGrid import UIGrid


class UIGrid_test(unittest.TestCase):

	def testWithAutoPos(self):
		cellSize = (10, 10)
		# test without maxNItems being set
		grid = UIGrid((3,2), cellSize)
		self.assertEqual(grid.getMaxNItems(), 6)
		self.assertEqual(grid.getNItems(), 0)
		self.assertEqual(grid.isFull(), False)
		self.assertEqual(grid.addItem("sheep"), (0,0))
		self.assertEqual(grid.addItem("cow"), (10, 0))
		self.assertEqual(grid.addItem("pig"), (20, 0))
		self.assertEqual(grid.getNItems(), 3)
		self.assertEqual(grid.getMaxNItems(), 6)
		self.assertEqual(grid.getFirstFreeGridPos(), (0, 1))
		self.assertEqual(grid.addItem("horse"), (0, 10))
		self.assertEqual(grid.addItem("chicken"), (10, 10))
		self.assertEqual(grid.isFull(), False)
		self.assertEqual(grid.getFirstFreeGridPos(), (2, 1))
		self.assertEqual(grid.addItem("dog"), (20, 10))
		self.assertEqual(grid.getNItems(), 6)
		self.assertEqual(grid.getMaxNItems(), 6)
		self.assertEqual(grid.isFull(), True)
		self.assertEqual(grid.addItem("donkey"), None) # grid should be full
		self.assertEqual(grid.getNItems(), 6)
		self.assertEqual(grid.getMaxNItems(), 6)
		self.assertEqual(grid.isFull(), True)
		self.assertFalse(grid.removeItem("cat"))
		self.assertEqual(grid.isFull(), True)
		self.assertTrue(grid.removeItem("cow"))
		self.assertEqual(grid.getNItems(), 5)
		self.assertEqual(grid.isFull(), False)
		self.assertEqual(grid.getFirstFreeGridPos(), (1, 0))
		self.assertFalse(grid.removeItem("cow"))
		self.assertEqual(grid.getNItems(), 5)
		self.assertTrue(grid.removeItem("pig"))
		self.assertTrue(grid.removeItem("horse"))
		self.assertEqual(grid.addItem("cat"), (10, 0))
		self.assertEqual(grid.getNItems(), 4)
		# test with ui offset and maxNItems smaller than grid
		grid = UIGrid((2,2), cellSize, uiOffsetPos=(5, 5), maxNItems=3)
		self.assertEqual(grid.getMaxNItems(), 3)
		self.assertEqual(grid.getNItems(), 0)
		self.assertEqual(grid.addItem("sheep"), (5,5))
		self.assertEqual(grid.addItem("sheep"), (15,5))
		self.assertEqual(grid.isFull(), False)
		self.assertEqual(grid.addItem("cow"), (5,15))
		self.assertEqual(grid.isFull(), True)
		self.assertEqual(grid.addItem("cow"), None) # full due to our "nSpaces" restriction
		self.assertEqual(grid.isFull(), True)
		self.assertEqual(grid.getMaxNItems(), 3)
		self.assertEqual(grid.getNItems(), 3)
		self.assertTrue(grid.removeItem("sheep")) # removing one sheep
		self.assertEqual(grid.isFull(), False)
		self.assertEqual(grid.addItem("cow"), (5,5)) # should take the position that was freed by the first sheep
		self.assertEqual(grid.isFull(), True)
		self.assertEqual(grid.addItem("cow"), None) # again full due to our "nSpaces" restriction
		self.assertEqual(grid.isFull(), True)
		self.assertEqual(grid.getMaxNItems(), 3)
		self.assertEqual(grid.getNItems(), 3)
		# test with maxNItems larger than grid (allow grow nColumns)
		grid = UIGrid((1,2), cellSize, maxNItems=3, autoGrow="columns")
		self.assertEqual(grid.getMaxNItems(), 3)
		self.assertEqual(grid.getNItems(), 0)
		self.assertEqual(grid.addItem("sheep"), (0,0))
		self.assertEqual(grid.addItem("cow"), (0,10))
		self.assertEqual(grid.growthHappened(), False)
		self.assertEqual(grid.isFull(), False)
		self.assertEqual(grid.addItem("horse"), (10,0)) # should trigger growth
		self.assertEqual(grid.growthHappened(), True)
		self.assertEqual(grid.growthHappened(clearFlag = True), True)
		self.assertEqual(grid.growthHappened(clearFlag = True), False)
		self.assertEqual(grid.addItem("dog"), None) # reached maxNItems
		self.assertEqual(grid.isFull(), True)
		# test with maxNItems larger than grid (autoGrow nRows instead)
		grid = UIGrid((1,2), cellSize, maxNItems=3, autoGrow="rows")
		self.assertEqual(grid.addItem("sheep"), (0,0))
		self.assertEqual(grid.addItem("cow"), (0,10))
		self.assertEqual(grid.growthHappened(), False)
		self.assertEqual(grid.isFull(), False)
		self.assertEqual(grid.addItem("horse"), (0,20)) # should trigger growth
		self.assertEqual(grid.isFull(), True)

	def testWithManualPos(self):
		cellSize = (5, 5)
		grid = UIGrid((2,2), cellSize, autoGrow="columns_first")
		self.assertEqual(grid.getNItems(), 0)
		self.assertEqual(grid.getMaxNItems(), 4)
		grid.setItemAt((1, 0), "foo")
		grid.setItemAt((1, 1), "bar1")
		self.assertEqual(grid.getNItems(), 2)
		self.assertEqual(grid.getItemAt((0, 0)), None)
		self.assertEqual(grid.getItemAt((1, 0)), "foo")
		self.assertEqual(grid.getItemAt((0, 1)), None)
		self.assertEqual(grid.getItemAt((1, 1)), "bar1")
		grid.setItemAt((1, 0), "bar2")
		self.assertEqual(grid.getNItems(), 2)
		self.assertEqual(grid.getMaxNItems(), 4)
		self.assertEqual(grid.getItemAt((1, 0)), "bar2")
		# test autogrow
		grid.setItemAt((4, 4), "bob")
		self.assertEqual(grid.getNItems(), 3)
		self.assertEqual(grid.getItemAt((3, 4)), None)
		self.assertEqual(grid.getItemAt((4, 4)), "bob")

	def testGridPos(self):
		grid = UIGrid((2,3), (5, 5)) # grid size (2,3)
		with self.assertRaises(ValueError):
			grid.validateGridPos((-1, 0))
		with self.assertRaises(ValueError):
			grid.validateGridPos((0, -1))
		grid.validateGridPos((0, 0))
		grid.validateGridPos((1, 0))
		grid.validateGridPos((0, 2))
		grid.validateGridPos((1, 2))
		with self.assertRaises(ValueError):
			grid.validateGridPos((2, 0))
		with self.assertRaises(ValueError):
			grid.validateGridPos((0, 3))
		with self.assertRaises(ValueError):
			grid.validateGridPos((2, 3))
		
		self.assertEqual(grid.nextGridPos((0, 0)), (1, 0))
		self.assertEqual(grid.nextGridPos((1, 0)), (0, 1))
		self.assertEqual(grid.nextGridPos((0, 1)), (1, 1))
		self.assertEqual(grid.nextGridPos((1, 1)), (0, 2))
		self.assertEqual(grid.nextGridPos((0, 2)), (1, 2))
		self.assertEqual(grid.nextGridPos((1, 2)), None)

		gridPos = (0, 0)
		self.assertEqual(grid.getNColumns() * grid.getNRows(), 6)
		for i in range(5): # iterate all cells except last one
			prevGridPos = gridPos
			gridPos = grid.nextGridPos(gridPos)
			self.assertEqual(prevGridPos, grid.prevGridPos(gridPos))
		self.assertEqual(grid.nextGridPos(gridPos), None) # check that it was indeed last

	def testCollapse(self):
		grid = UIGrid((2,3), (5, 5)) # grid size (2,3)
		grid.setItemAt((0,0), "A")
		grid.setItemAt((0,1), "B")
		grid.setItemAt((1,1), "C")
		grid.setItemAt((1,2), "D")
		self.assertEqual(grid.getNItems(), 4)
		self.assertEqual(grid.getFirstFreeGridPos(), (1,0))
		self.assertEqual(grid.getFirstTakenGridPos(), (0,0))
		movedItemsTuples = grid.collapse()
		self.assertEqual(grid.getNItems(), 4)
		self.assertEqual(movedItemsTuples, [("B",(5, 0)), ("C",(0, 5)), ("D",(5, 5))])
		self.assertEqual(grid.getItemAt((0,0)), "A")
		self.assertEqual(grid.getItemAt((1,0)), "B")
		self.assertEqual(grid.getItemAt((0,1)), "C")
		self.assertEqual(grid.getItemAt((1,1)), "D")
		self.assertEqual(grid.getFirstFreeGridPos(), (0,2))
		self.assertEqual(grid.getFirstTakenGridPos(), (0,0))
		
	def runTest(self):
		self.testGridPos()
		self.testWithAutoPos()
		self.testWithManualPos()
		self.testCollapse()

if __name__ == '__main__':
	unittest.main()
