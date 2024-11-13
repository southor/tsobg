
import unittest

from .UIInterface import UIInterface
from .GridLayout import GridLayout
from .GameObject import GameObject


class GridLayout_test(unittest.TestCase):
	
	def _swapInList(lst, index1, index2):
		item1 = lst[index1]
		item2 = lst[index2]
		lst[index1] = item2
		lst[index2] = item1

	def _fillLayout(self, uiInterface, gridLayout, nObjects):
		gl = gridLayout
		objs = [GameObject(uiInterface, "obj" + str(i)) for i in range(nObjects)]
		for obj in objs:
			gl.addObject(obj)
		return objs
	
	def _testOccupied(self, uiInterface):
		gl = GridLayout((3,4), (10,5))
		objs = self._fillLayout(uiInterface, gl, 7)
		# remember, coordinates are always as (colN,rowN), and grid is stored row by row
		placeVerifies = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2)]
		for obj,place in zip(objs, placeVerifies):
			self.assertTrue(obj is gl.getObjectAt(place))
		# grid looks like [[X,X,X],[X,X,X],[X,-,-],[-,-,-]]
		self.assertTrue(gl.hasObject(objs[4])) # object at (1,1)
		self.assertTrue(gl.getObjectAt((1,1)) is objs[4])
		self.assertTrue(gl.getObjectAt((1,1)) != None)
		self.assertEqual(gl.getFirstTakenPlace(), (0,0))
		self.assertEqual(gl.getFirstFreePlace(), (1,2))
		self.assertEqual(gl.getFirstTakenPlace((1,1)), (1,1))
		gl.removeObjectAt((1,1))
		# grid looks like [[X,X,X],[X,-,X],[X,-,-],[-,-,-]]
		self.assertFalse(gl.hasObject(objs[4])) # object at (1,1)
		self.assertEqual(gl.getObjectAt((1,1)), None)
		self.assertEqual(gl.getFirstTakenPlace(), (0,0))
		self.assertEqual(gl.getFirstFreePlace(), (1,1))
		self.assertEqual(gl.getFirstTakenPlace((1,1)), (2,1))
		gl.removeObjectAt((0,0))
		# grid looks like [[-,X,X],[X,-,X],[X,-,-],[-,-,-]]
		self.assertEqual(gl.getFirstTakenPlace(), (1,0))
		self.assertEqual(gl.getFirstFreePlace(), (0,0))
		self.assertEqual(gl.getFirstTakenPlace((1,1)), (2,1))
		gl.swap((0,0), (0,1)) # swap obj0 with obj3
		GridLayout_test._swapInList(objs, 0, 3) # also swap in objs list to make verifying easier later on
		# grid looks like [[X,X,X],[-,-,X],[X,-,-],[-,-,-]]
		self.assertEqual(gl.getFirstTakenPlace(), (0,0))
		self.assertEqual(gl.getFirstFreePlace(), (0,1))
		self.assertEqual(gl.getFirstTakenPlace((1,1)), (2,1))
		gl.removeObjectAt((2,1))
		# grid looks like [[X,X,X],[-,-,-],[X,-,-],[-,-,-]]
		self.assertEqual(gl.getFirstTakenPlace((1,1)), (0,2))
		self.assertEqual(gl.getFirstFreePlace((2,0)), (0,1))
		self.assertEqual(gl.getFirstFreePlace((0,1)), (0,1))
		self.assertEqual(gl.getFirstFreePlace((1,1)), (1,1))
		self.assertEqual(gl.getFirstFreePlace((2,1)), (2,1))
		self.assertEqual(gl.getFirstFreePlace((0,2)), (1,2))
		collapseRes = gl.collapse()
		# obj at (0,2) should have moved to (0,1)
		# grid looks like [[X,X,X],[X,-,-],[-,-,-],[-,-,-]]
		placeVerifies = [(0,0), (1, 0), (2, 0), None, None, None, (0, 1)] # the new locations for the objects in objs
		for obj,place in zip(objs, placeVerifies):
			if place:
				self.assertTrue(gl.hasObject(obj))
				self.assertTrue(obj is gl.getObjectAt(place))
			else:
				self.assertFalse(gl.hasObject(obj))

	def _verifyVisitShortcut(self, gridLayout, startGridPos, placeVerifies, cellsVerifies):
		i = 0
		def visitFunc(gridPos, cell):
			nonlocal i
			if i >= len(placeVerifies):
				return i
			self.assertEqual(gridPos, placeVerifies[i])
			self.assertTrue(cell is cellsVerifies[i])
			i += 1
			return None
		res = gridLayout.visitCellsShortcut(visitFunc, startGridPos=startGridPos)
		self.assertEqual(res, len(placeVerifies))

	def _verifyVisitReduce(self, gridLayout, startGridPos, placeVerifies, cellsVerifies):
		i = 0
		def visitFunc(gridPos, cell, res):
			nonlocal i
			if i < len(placeVerifies):
				self.assertEqual(gridPos, placeVerifies[i])
				self.assertTrue(cell is cellsVerifies[i])
			i += 1
			return res + [cell]
		res = gridLayout.visitCellsReduce(visitFunc, initRes=[], startGridPos=startGridPos)
		#print([el.getDivID() if el else None for el in res])
		#print([el.getDivID() if el else None for el in cellsVerifies])
		self.assertEqual(res, cellsVerifies)

	def _testVisit(self, uiInterface):
		gl = GridLayout((3,4), (10,5))
		objs = self._fillLayout(uiInterface, gl, 8)
		placeVerifies = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2)]
		self._verifyVisitShortcut(gl, (1, 1), placeVerifies[4:7], objs[4:7])
		gl.removeObjectAt((0,0))
		gl.removeObjectAt((0,1))
		gl.removeObjectAt((1,1))
		objs = [None, objs[1], objs[2], None, None, objs[5], objs[6], objs[7]]
		placeVerifies += [(2, 2), (0, 3), (1, 3), (2, 3)] * 4 # we will traverse 4 empty cells at the end
		objs += [None] * 4 # we will traverse 4 empty cells at the end
		self._verifyVisitReduce(gl, (1, 1), placeVerifies[4:], objs[4:])

	def _testPadding(self, uiInterface):
		gl = GridLayout((3,5), (10,5), padding=(4,4))
		self._fillLayout(uiInterface, gl, 14)
		self.assertEqual(gl.getNObjects(), 14)
		obj = gl.getObjectAt((1,2))
		obj.setPos((1, 2))
		self.assertEqual(obj.getEffectivePos(), (15, 16))
		obj = gl.getObjectAt((1,3))
		self.assertEqual(obj.getEffectivePos(), (14, 19))

	def runTest(self):
		uiInterface = UIInterface()
		self._testOccupied(uiInterface)
		self._testVisit(uiInterface)
		self._testPadding(uiInterface)


		

if __name__ == '__main__':
	unittest.main()