

import unittest

from .UIInterface import UIInterface
from .FreeLayout import FreeLayout
from .GameObject import GameObject


class FreeLayout_test(unittest.TestCase):

	def _fillLayout(self, uiInterface, freeLayout, nObjects):
		fl = freeLayout
		self.assertEqual(fl.getNObjects(), 0)
		self.assertEqual(fl.getFirstObject(), None)
		objs = [GameObject(uiInterface, "obj" + str(i)) for i in range(nObjects)]
		for obj in objs:
			fl.addObject(obj)
		self.assertFalse(fl.getObjectAt(1) is objs[0])
		# should have indexes in correct order
		for i,obj in enumerate(objs):
			self.assertTrue(fl.hasObject(obj))
			self.assertTrue(fl.getObjectAt(i) is obj)
			self.assertEqual(fl.getObjectPlace(obj), i)
		self.assertTrue(fl.getFirstObject() is objs[0])
		self.assertEqual(fl.getNObjects(), nObjects)
		return objs

	def _testIndexes(self, uiInterface):
		fl = FreeLayout()
		objs = self._fillLayout(uiInterface, fl, 5)
		self.assertEqual(fl.getNObjects(), 5)
		# removing objects in between
		fl.removeObject(objs[1])
		fl.removeObjectAt(3)
		self.assertEqual(fl.getNObjects(), 3)
		# verify correct one was removed and getObjectAt returns None for those indexes
		self.assertTrue(fl.getFirstObject() is objs[0])
		self.assertTrue(fl.getObjectAt(0) is objs[0])
		self.assertEqual(fl.getObjectAt(1), None)
		self.assertTrue(fl.getObjectAt(2) is objs[2])
		self.assertEqual(fl.getObjectAt(3), None)
		# verify hasObject for removed and those still there
		self.assertTrue(fl.hasObject(objs[0]))
		self.assertFalse(fl.hasObject(objs[1]))
		self.assertTrue(fl.hasObject(objs[2]))
		self.assertFalse(fl.hasObject(objs[3]))
		# add object again should insert at first free place
		objs[1] = GameObject(uiInterface, "newObj1")
		fl.addObject(objs[1])
		self.assertEqual(fl.getNObjects(), 4)
		self.assertEqual(fl.getObjectPlace(objs[1]), 1)
		self.assertTrue(fl.hasObject(objs[1]))
		self.assertEqual(fl.getObjectPlace(objs[3]), None)
		# test getFirstObject method
		self.assertTrue(fl.getFirstObject() is objs[0])
		self.assertTrue(fl.getFirstObject() is objs[0])
		self.assertTrue(fl.getFirstObject(remove=True) is objs[0])
		self.assertTrue(fl.getFirstObject() is objs[1])
		self.assertTrue(fl.getFirstObject(remove=True) is objs[1])
		self.assertTrue(fl.getFirstObject(remove=True) is objs[2])
		self.assertTrue(fl.getFirstObject() is objs[4]) # skipped objs[3] because that one was removed (and never repalced)
		self.assertEqual(fl.getNObjects(), 1)
	
	def _testVisitor(self, uiInterface):
		fl = FreeLayout()
		objs = self._fillLayout(uiInterface, fl, 4)
		
		def visitFunc1(pos, cell, prevRes):
			self.assertEqual(prevRes+1, pos)
			self.assertTrue(cell, objs[pos])
			return pos
		fl.visitCellsReduce(visitFunc1, -1)
		fl.removeObjectAt(0)
		fl.visitObjectsReduce(visitFunc1, 0)
		
		prevPos = 0
		def visitFunc2(pos, cell):
			nonlocal prevPos
			self.assertEqual(prevPos+1, pos)
			self.assertTrue(cell, objs[pos])
			prevPos = pos
		fl.removeAllObjects(visitFunc=visitFunc2)

		self.assertEqual(fl.getFirstObject(), None)
		self.assertEqual(fl.getNObjects(), 0)
		for obj in objs:
			self.assertFalse(fl.hasObject(obj))
		
	def _testSetObjectAt(self, uiInterface):
		""" Test setObjectAt with limited maxNItems """
		fl = FreeLayout(maxNItems=5)
		objs = self._fillLayout(uiInterface, fl, 3) # fill up with 3 (so is room for 2 more)
		newObj2 = GameObject(uiInterface, "newObj2")
		self.assertEqual(fl.setObjectAt(2, newObj2), (True, objs[2])) # replacing existing
		self.assertEqual(fl.setObjectAt(2, newObj2), (True, newObj2)) # replacing itself
		self.assertFalse(fl.hasObject(objs[2]))
		self.assertTrue(fl.hasObject(newObj2))
		self.assertEqual(fl.getObjectPlace(objs[2]), None)
		self.assertEqual(fl.getObjectPlace(newObj2), 2)
		self.assertEqual(fl.getNObjects(), 3)
		self.assertEqual(fl.setObjectAt(1, None), (True, objs[1])) # removing object
		self.assertEqual(fl.setObjectAt(1, None), (False, None)) # no object was removed (should return False)
		self.assertEqual(fl.getNObjects(), 2)
		self.assertFalse(fl.hasObject(objs[1]))
		self.assertTrue(fl.hasObject(newObj2))
		self.assertTrue(fl.addObject(GameObject(uiInterface, "newObj1")))
		self.assertTrue(fl.addObject(GameObject(uiInterface, "newObj3")))
		self.assertTrue(fl.addObject(GameObject(uiInterface, "newObj4")))
		self.assertEqual(fl.getNObjects(), 5)
		self.assertFalse(fl.addObject(GameObject(uiInterface, "newObj4"))) # should return False because layout is full
		self.assertEqual(fl.getNObjects(), 5)
		self.assertEqual(fl.setObjectAt(2, None, allowReplace=False), (True,newObj2)) # removing object still allowed
		newObj3 = fl.getObjectAt(3)
		self.assertEqual(newObj3.getDivID(), "newObj3")
		self.assertEqual(fl.setObjectAt(3, GameObject(uiInterface, "newObj3b"), allowReplace=False), (False,newObj3)) # replacing object not allowed
		self.assertEqual(fl.removeObjectAt(3), newObj3) # removing object always allowed
		

	def runTest(self):
		uiInterface = UIInterface()
		self._testIndexes(uiInterface)
		self._testVisitor(uiInterface)
		self._testSetObjectAt(uiInterface)


		

if __name__ == '__main__':
	unittest.main()