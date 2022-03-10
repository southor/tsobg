import unittest
from unittest.mock import patch

import sys
from pathlib import Path
pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent))
sys.path.append(str(pathHere.parent.parent))

import board_data

from MainBoard import MainBoard

@patch('tsobg.UIInterface')

class MainBoard_test(unittest.TestCase):

	def testMapShape(self, uiInterface):
		mainBoard = MainBoard(uiInterface)
		
		# test that we can access all expected tiles (we expect map to be a rectangle) and compare grid tiles to original map
		
		nRows = mainBoard.getNRows()
		nCols = mainBoard.getNColumns()
		
		#mapCounts = {board_data.WATER:0, board_data.GREEN:0, board_data.PARKING:0, board_data.LOT:0}
		#for tile in MainBoard.__map:
		#	mapCounts[tile] += 1
		
		#gridCounts = {board_data.WATER:0, board_data.GREEN:0, board_data.PARKING:0, board_data.LOT:0}
		for tileY in range(0, nRows):
			for tileX in range(0, nCols):
				tileType = mainBoard.getTileType(tileX, tileY)
				#gridCounts[tile] += 1
				self.assertEqual(tileType, board_data.map[tileY][tileX]) # all tiles should be like the map
				floors = mainBoard.getFloors(tileX, tileY)
				if tileType == board_data.LOT:
					self.assertTrue(mainBoard.isLot(tileX, tileY)) # test isLot
					self.assertEqual(type(floors), list) # Lots always returns a list here
					self.assertEqual(floors, []) # map is always empty at start
				else:
					self.assertFalse(mainBoard.isLot(tileX, tileY)) # test isLot
					self.assertEqual(floors, None) # Should be empty for none lots


	def testFloorChanges(self, uiInterface):
		mainBoard = MainBoard(uiInterface)
		tileX,tileY = 3,1
		floors = mainBoard.getFloors(tileX, tileY)
		self.assertEqual(floors, []) # make sure we are using an unbuilt spot for the test
		self.assertTrue(mainBoard.isEmptyLot(tileX,tileY))
		self.assertFalse(mainBoard.isBuiltLot(tileX,tileY))
		# modify floors 1
		floors = ["shop", "office"]
		mainBoard.setFloors(tileX, tileY, floors)
		# test result 1
		floorsB = mainBoard.getFloors(tileX, tileY)
		self.assertEqual(floors, floorsB)
		self.assertFalse(floors is floorsB) # should have made a copy
		self.assertFalse(mainBoard.isEmptyLot(tileX,tileY))
		self.assertTrue(mainBoard.isBuiltLot(tileX,tileY))
		# modify floors 2
		floors = floors + ["apartment"]
		mainBoard.setFloors(tileX, tileY, floors)
		# test result 2
		floorsB = mainBoard.getFloors(tileX, tileY)
		self.assertEqual(floors, floorsB)
		self.assertFalse(floors is floorsB) # should have made a copy

	def runTest(self):
		self.testMapShape()
		self.testFloorChanges()



