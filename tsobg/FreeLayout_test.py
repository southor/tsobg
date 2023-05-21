

import unittest

from .UIInterface import UIInterface
from .FreeLayout import FreeLayout
from .GameObject import GameObject


class FreeLayout_test(unittest.TestCase):

	def _fillLayout(self, uiInterface, freelayout, nObjects):
		fl = freelayout
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
			self.assertEqual(fl.getObjectCoordinates(obj), i)
		self.assertTrue(fl.getFirstObject() is objs[0])
		self.assertEqual(fl.getNObjects(), nObjects)
		return objs

	def _testIndexes(self, uiInterface):
		fl = FreeLayout()
		objs = self._fillLayout(uiInterface, fl, 5)
		#fl = FreeLayout()
		#self.assertEqual(fl.getNObjects(), 0)
		#self.assertEqual(fl.getFirstObject(), None)
		#objs = [GameObject(uiInterface, "obj" + str(i)) for i in range(5)]
		#for obj in objs:
		#	fl.addObject(obj)
		#self.assertFalse(fl.getObjectAt(1) is objs[0])
		## should have indexes in correct order
		#for i,obj in enumerate(objs):
		#	self.assertTrue(fl.hasObject(obj))
		#	self.assertTrue(fl.getObjectAt(i) is obj)
		#	self.assertEqual(fl.getObjectCoordinates(obj), i)
		#self.assertTrue(fl.getFirstObject() is objs[0])
		self.assertEqual(fl.getNObjects(), 5)
		# removing objects in between
		fl.removeObject(objs[1])
		fl.removeObject(objs[3]) # replace later with fl.removeObjectAt(3) ?
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
		self.assertEqual(fl.getObjectCoordinates(objs[1]), 1)
		self.assertTrue(fl.hasObject(objs[1]))
		self.assertEqual(fl.getObjectCoordinates(objs[3]), None)
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
		

	def runTest(self):
		uiInterface = UIInterface()
		self._testIndexes(uiInterface)
		self._testVisitor(uiInterface)


		

if __name__ == '__main__':
	unittest.main()