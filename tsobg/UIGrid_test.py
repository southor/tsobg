import unittest

if __name__ == '__main__':
	from UIGrid import UIGrid
else:
	from .UIGrid import UIGrid


class UIGrid_test(unittest.TestCase):
	
	def runTest(self):
		cellSize = (10, 10)
		grid = UIGrid(2, 3, cellSize)
		self.assertEqual(grid.getNSpaces(), 6)
		self.assertEqual(grid.getNOccupied(), 0)
		self.assertEqual(grid.getNUnoccupied(), 6)
		self.assertEqual(grid.addItem("sheep"), (0,0))
		self.assertEqual(grid.addItem("cow"), (10, 0))
		self.assertEqual(grid.getNUnoccupied(), 4)
		self.assertEqual(grid.addItem("pig"), (20, 0))
		self.assertEqual(grid.getNOccupied(), 3)
		self.assertEqual(grid.getNSpaces(), 6)
		self.assertEqual(grid.addItem("horse"), (0, 10))
		self.assertEqual(grid.addItem("chicken"), (10, 10))
		self.assertEqual(grid.addItem("dog"), (20, 10))
		self.assertEqual(grid.removeItem("cat"), False)
		self.assertEqual(grid.removeItem("cow"), True)
		self.assertEqual(grid.getNOccupied(), 5)
		self.assertEqual(grid.removeItem("cow"), False)
		self.assertEqual(grid.getNOccupied(), 5)
		self.assertEqual(grid.removeItem("pig"), True)
		self.assertEqual(grid.removeItem("horse"), True)
		self.assertEqual(grid.addItem("cat"), (10, 0))
		self.assertEqual(grid.getNOccupied(), 4)

if __name__ == '__main__':
	unittest.main()
