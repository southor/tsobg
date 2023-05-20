

import unittest

from .UIInterface import UIInterface
from .FreeLayout import FreeLayout
from .GameObject import GameObject

class FreeLayout_test(unittest.TestCase):

	def testIndexes(self, uiInterface):
		fl = FreeLayout()
		self.assertEqual(fl.getNObjects(), 0)
		self.assertEqual(fl.getFirstObject(), None)
		objs = [GameObject(uiInterface, "obj" + str(i)) for i in range(5)]
		for obj in objs:
			fl.addObject(obj)
		self.assertFalse(fl.getObjectAt(1) is objs[0])
		# should have indexes in correct order
		for i,obj in enumerate(objs):
			self.assertTrue(fl.hasObject(obj))
			self.assertTrue(fl.getObjectAt(i) is obj)
			self.assertEqual(fl.getObjectCoordinates(obj), i)
		self.assertTrue(fl.getFirstObject() is objs[0])
		# removing objects in between
		fl.removeObject(objs[1])
		fl.removeObject(objs[3]) # repalce later with fl.removeObjectAt(3) ?
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
		# TODO remove objects and eventually verify that fl.getFirstObject() returns None

	def runTest(self):
		uiInterface = UIInterface()
		self.testIndexes(uiInterface)
		

if __name__ == '__main__':
	unittest.main()