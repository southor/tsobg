
import unittest

from .UIInterface import UIInterface
from .GameObject import GameObject
from .FreeLayout import FreeLayout
from .GridLayout import GridLayout


class GameObject_test(unittest.TestCase):
	
	# def _testFlags(self):
		# go = GameObject(UIInterface(), "testobj")
		# # test default flag values
		# self.assertTrue(go.getFlag("visible"))
		# self.assertTrue(go.getFlag("trapClicks"))
		# self.assertFalse(go.getFlag("selectable"))
		# self.assertEqual(go.getFlags(), {"visible", "trapClicks"})
		# # test modify flag values
		# go.setFlags("selectable")
		# self.assertEqual(go.getFlags(), {"visible", "trapClicks", "selectable"})
		# go.setFlags({"selectable"})
		# self.assertEqual(go.getFlags(), {"selectable"})
		# go.setFlags("visible")
		# self.assertEqual(go.getFlags(), {"visible", "selectable"})
		# go.setFlags(visible=False)
		# self.assertEqual(go.getFlags(), {"selectable"})
		# go.setFlags({"trapClicks"}, trapClicks=False)
		# self.assertEqual(go.getFlags(), set())
		# # Reset to new GameObject, test more modify flag values
		# go = GameObject(UIInterface(), "testobj")
		# self.assertEqual(go.getFlags(), {"visible", "trapClicks"})
		# go.setFlags(set(), "trapClicks", "visible", trapClicks=False)
		# self.assertEqual(go.getFlags(), {"visible"})
		# go.setFlags({"visible", "selectable"}, {"selectable":False})
		# self.assertEqual(go.getFlags(), {"visible"})
		# go.setFlags({"visible", "selectable"}, {"selectable":False}, "selectable")
		# self.assertEqual(go.getFlags(), {"visible", "selectable"})
		# self.assertTrue(go.getFlag("visible"))
		# self.assertTrue(go.getFlag("selectable"))
		# self.assertFalse(go.getFlag("trapClicks"))
		
	def _testFlags(self):
		go = GameObject(UIInterface(), "testobj")
		# test default flag values
		self.assertTrue(go.getFlag("visible"))
		self.assertEqual(go.getFlags(), {"visible"})
		# test modify flag values
		go.setFlags(visible=False)
		self.assertEqual(go.getFlags(), set())
		go.setFlags("visible")
		self.assertTrue(go.getFlag("visible"))
		go.setFlags(set())
		self.assertFalse(go.getFlag("visible"))

	def _gridPosToStr(gridPos):
		return str(gridPos[0]) + str(gridPos[1])

	def _testChildren(self):
		uiInterface = UIInterface()
		p = GameObject(uiInterface, "parent", layout=GridLayout((2,2), (50,50)), size=(100, 100))
		c00 = GameObject(uiInterface, "child00", size=(40,40))
		c10= GameObject(uiInterface, "child10", size=(40,40))
		c01 = GameObject(uiInterface, "child01", size=(40,40))
		c11 = GameObject(uiInterface, "child11", size=(40,40))
		p.addChild(c00)
		p.addChild(c10)
		p.addChild(c01)
		p.addChild(c11)
		self.assertEqual(p.getChildCoordinates(c00), (0, 0))
		self.assertEqual(p.getChildCoordinates(c11), (1, 1))
		self.assertTrue(p.getStackObject("child00") is c00)
		self.assertTrue(p.getStackObject("child01") is c01)
		self.assertTrue(p.getChild("child10") is c10)
		self.assertTrue(p.getChild("child11") is c11)
		self.assertTrue(p.getChildAt((1, 0)) is c10)
		self.assertEqual(p.getNChildren(), 4)
		self.assertTrue(p.hasChild(c00))
		self.assertTrue(p.getFirstChild() is c00)
		p.removeChildAt((0, 0))
		self.assertFalse(p.hasChild(c00))
		self.assertFalse(p.getChild("child00"))
		self.assertTrue(p.getFirstChild() is c10)

		self.assertEqual(p.getNChildren(), 3)
		nVisitedDuringRemove = 0
		def removedVisitor(pos, child):
			self.assertEqual("child" + GameObject_test._gridPosToStr(pos), child.getDivID())
			nonlocal nVisitedDuringRemove
			nVisitedDuringRemove += 1
		p.removeAllChildren(visitFunc=removedVisitor)
		self.assertEqual(nVisitedDuringRemove, 3)
		self.assertEqual(p.getNChildren(), 0)
		self.assertTrue(p.getFirstChild() is None)

	def _testGrandchild(self):
		# test: FreeLayout, FreeLayout
		uiInterface = UIInterface()
		p = GameObject(uiInterface, "parent", size=(20, 20))
		c = GameObject(uiInterface, "child", parent=p, pos=(5, 0), size=(10, 10))
		gc = GameObject(uiInterface, "grandchild", pos=(3, 0), size=(5, 5))
		c.addChild(gc)
		self.assertEqual(p.getLayoutType(), FreeLayout)
		self.assertEqual(c.getLayoutType(), FreeLayout)
		self.assertEqual(gc.getLayoutType(), FreeLayout)
		self.assertEqual(c.getParent(), p)
		self.assertEqual(gc.getParent(), c)
		self.assertTrue(p.getFirstChild() is c)
		self.assertTrue(c.getFirstChild() is gc)
		self.assertTrue(p.hasChild(c))
		self.assertTrue(gc.inStackOf(p))
		self.assertFalse(p.hasChild(gc))
		self.assertEqual(c.getChildCoordinates(gc), 0)
		self.assertEqual(p.getChildCoordinates(c), 0)
		p.addChild(GameObject(uiInterface, "child1"))
		self.assertEqual(p.getChildCoordinates(p.getChild("child1")), 1)
		self.assertEqual(p.getChildCoordinates(gc), None)
		self.assertEqual(p.getStackCoordinatesFor(c), [0])
		self.assertEqual(p.getStackCoordinatesFor(gc), [0, 0])
		self.assertTrue(p.getStackObject("grandchild") is gc)
		# test: GridLayout, FreeLayout
		p.removeChild(c)
		self.assertEqual(c.getParent(), None)
		layout = GridLayout((5, 5), (20, 20))
		p = GameObject(uiInterface, "parent", layout=layout, size=(100, 100))
		p.setChildAt((0, 2), c)
		self.assertEqual(p.getLayoutType(), GridLayout)
		self.assertEqual(c.getLayoutType(), FreeLayout)
		self.assertEqual(gc.getLayoutType(), FreeLayout)
		self.assertFalse(p.hasChild(gc))
		self.assertFalse(gc.hasChild(p))
		self.assertTrue(gc.inStackOf(p))
		self.assertTrue(c.inStackOf(p))
		self.assertTrue(p.inStackOf(p))
		self.assertTrue(p.inStackOf(p.getDivID()))
		self.assertFalse(p.inStackOf(c))
		self.assertFalse(p.inStackOf(c.getDivID()))
		self.assertEqual(c.getChildCoordinates(gc), 0)
		self.assertEqual(c.getStackCoordinatesFor(gc), [0])
		self.assertEqual(p.getChildCoordinates(c), (0, 2))
		self.assertEqual(p.getChildCoordinates(gc), None)
		self.assertEqual(p.getStackCoordinatesFor(gc), [(0, 2), 0])
		self.assertEqual(p.getStackCoordinatesFor(gc.getDivID()), [(0, 2), 0])
		self.assertTrue(p.getStackObjectAt([(0, 2), 0]) is gc)
		self.assertEqual(c.getLayoutPos(), (0, 40)) # layoutPos of child should have been set by GridLayout (grid pos multiplied by tile size)
		p.setChildAt((0, 2), None) # remove child by setChildAt
		self.assertFalse(p.hasChild(c))
		self.assertFalse(c.inStackOf(p))
		self.assertTrue(c.hasChild(gc))
		self.assertTrue(gc.inStackOf(c))
		self.assertEqual(p.getNChildren(), 0)
		self.assertEqual(c.getNChildren(), 1)
		p.removeAllChildren()
		self.assertEqual(p.getNChildren(), 0)
		self.assertEqual(c.getNChildren(), 1)

	def _testMoveToNewParent(self):
		uiInterface = UIInterface()
		p1 = GameObject(uiInterface, "parent1", size=(20, 20), layout=GridLayout((5, 5), (5, 5)))
		p2 = GameObject(uiInterface, "parent2", size=(50, 50), layout=FreeLayout())
		obj = GameObject(uiInterface, "obj1", size=(5, 5))
		self.assertEqual(obj.getLayoutPos(), ("auto", "auto"))
		# add child into grid
		p1.setChildAt((2, 1), obj)
		self.assertTrue(p1.hasChild(obj))
		self.assertEqual(p1.getChildCoordinates(obj), (2, 1))
		self.assertEqual(obj.getLayoutPos(), (10, 5))
		self.assertEqual(obj.getEffectivePos(), (10, 5))
		# apply position offsetting 
		obj.setPos((2, 2))
		self.assertEqual(obj.getLayoutPos(), (10, 5))
		self.assertEqual(obj.getEffectivePos(), (12, 7))
		# move child to new parent
		obj.setParent(p2)
		self.assertFalse(p1.hasChild(obj))
		self.assertTrue(p2.hasChild(obj))
		self.assertEqual(p1.getChildCoordinates(obj), None)
		self.assertEqual(p2.getChildCoordinates(obj), 0)
		self.assertEqual(obj.getLayoutPos(), ("auto", "auto"))

	def runTest(self):
		self._testFlags()
		self._testChildren()
		self._testGrandchild()
		self._testMoveToNewParent()
