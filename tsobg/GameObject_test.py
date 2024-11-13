
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
		p = GameObject(uiInterface, "parent", childrenLayout=GridLayout((2,2), (50,50)), size=(100, 100))
		c00 = GameObject(uiInterface, "child00", size=(40,40))
		c10= GameObject(uiInterface, "child10", size=(40,40))
		c01 = GameObject(uiInterface, "child01", size=(40,40))
		c11 = GameObject(uiInterface, "child11", size=(40,40))
		self.assertEqual(c01.getEffectivePos(), ("auto", "auto"))
		p.addChild(c00)
		p.addChild(c10)
		c11.setParent(p, (1,1)) # add child by using setParent with place (leaving a gap at (0,1))
		p.addChild(c01) # should get place=(0,1) since that gap was left 
		self.assertEqual(c01.getEffectivePos(), (0, 50))
		self.assertEqual(p.getChildPlace(c00), (0, 0))
		self.assertEqual(p.getChildPlace(c11), (1, 1))
		self.assertTrue(p.getStackObject("child00") is c00)
		self.assertTrue(p.getStackObject("child01") is c01)
		self.assertTrue(p.getChild("child10") is c10)
		self.assertTrue(p.getChild("child11") is c11)
		self.assertTrue(p.getChildAt((1, 0)) is c10)
		self.assertEqual(p.getNChildren(), 4)
		self.assertTrue(p.hasChild(c00))
		self.assertTrue(p.getFirstChild() is c00)
		self.assertTrue(p.removeChildAt((0, 0)) is c00)
		self.assertFalse(p.hasChild(c00))
		self.assertFalse(p.getChild("child00"))
		self.assertTrue(p.getFirstChild() is c10)
		self.assertEqual([c.getDivID() for c in p.getAllChildren()], ["child10", "child01", "child11"])
		self.assertEqual([p for p,c in p.getAllChildrenPlaceTuple()], [(1,0), (0,1), (1,1)])
		# test replacing children
		c01new = GameObject(uiInterface, "child01", size=(30,30)) # new child with the same divID as the previous one
		self.assertEqual(p.setChildAt((0,1), c01new, allowReplace=False), (False,c01))
		self.assertEqual(p.setChildAt((0,1), c01new, allowReplace=True), (True,c01))
		with self.assertRaises(ValueError):
			p.setChildAt((0,1), c01new, allowReplace=False) # cannot add a child that already has a parent
		with self.assertRaises(ValueError):
			p.setChildAt((0,1), c01new, allowReplace=True) # cannot add a child that already has a parent
		self.assertEqual(c01.getEffectivePos(), ("auto", "auto"))
		self.assertEqual(p.getNChildren(), 3)
		nVisitedDuringRemove = 0
		def removedVisitor(gridPos, child):
			self.assertEqual("child" + GameObject_test._gridPosToStr(gridPos), child.getDivID())
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
		self.assertEqual(p.getChildrenLayoutType(), FreeLayout)
		self.assertEqual(c.getChildrenLayoutType(), FreeLayout)
		self.assertEqual(gc.getChildrenLayoutType(), FreeLayout)
		self.assertEqual(c.getParent(), p)
		self.assertEqual(gc.getParent(), c)
		self.assertTrue(p.getFirstChild() is c)
		self.assertTrue(c.getFirstChild() is gc)
		self.assertTrue(p.hasChild(c))
		self.assertTrue(gc.inStackOf(p))
		self.assertFalse(p.hasChild(gc))
		self.assertEqual(c.getChildPlace(gc), 0)
		self.assertEqual(p.getChildPlace(c), 0)
		p.addChild(GameObject(uiInterface, "child1"))
		self.assertEqual(p.getChildPlace(p.getChild("child1")), 1)
		self.assertEqual(p.getChildPlace(gc), None)
		self.assertEqual(p.getStackCoordinatesFor(c), [0])
		self.assertEqual(p.getStackCoordinatesFor(gc), [0, 0])
		self.assertTrue(p.getStackObject("grandchild") is gc)
		# test: GridLayout, FreeLayout
		p.removeChild(c)
		self.assertEqual(c.getParent(), None)
		layout = GridLayout((5, 5), (20, 20))
		p = GameObject(uiInterface, "parent", childrenLayout=layout, size=(100, 100))
		self.assertEqual(p.setChildAt((0, 2), c), (True,None)) # add child to cell
		with self.assertRaises(ValueError):
			p.setChildAt((0, 2), c, allowReplace=False) # adding a child that already has parent not allowed
		self.assertEqual(p.getChildrenLayoutType(), GridLayout)
		self.assertEqual(c.getChildrenLayoutType(), FreeLayout)
		self.assertEqual(gc.getChildrenLayoutType(), FreeLayout)
		self.assertFalse(p.hasChild(gc))
		self.assertFalse(gc.hasChild(p))
		self.assertTrue(gc.inStackOf(p))
		self.assertTrue(c.inStackOf(p))
		self.assertTrue(p.inStackOf(p))
		self.assertTrue(p.inStackOf(p.getDivID()))
		self.assertFalse(p.inStackOf(c))
		self.assertFalse(p.inStackOf(c.getDivID()))
		self.assertEqual(c.getChildPlace(gc), 0)
		self.assertEqual(c.getStackCoordinatesFor(gc), [0])
		self.assertEqual(p.getChildPlace(c), (0, 2))
		self.assertEqual(p.getChildPlace(gc), None)
		self.assertEqual(p.getStackCoordinatesFor(gc), [(0, 2), 0])
		self.assertEqual(p.getStackCoordinatesFor(gc.getDivID()), [(0, 2), 0])
		self.assertTrue(p.getStackObjectAt([(0, 2), 0]) is gc)
		self.assertEqual(c.getLayoutPos(), (0, 40)) # layoutPos of child should have been set by GridLayout (grid pos multiplied by tile size)
		self.assertEqual(p.setChildAt((0, 2), None), (True,c)) # remove child by setChildAt
		self.assertFalse(p.hasChild(c))
		self.assertFalse(c.inStackOf(p))
		self.assertTrue(c.hasChild(gc))
		self.assertTrue(gc.inStackOf(c))
		self.assertEqual(p.getNChildren(), 0)
		self.assertEqual(c.getNChildren(), 1)
		p.removeAllChildren()
		self.assertEqual(p.getNChildren(), 0)
		self.assertEqual(c.getNChildren(), 1)

	def _testInitWithParent(self):
		uiInterface = UIInterface()
		c = GameObject(uiInterface, "child", parent="game_area")
		gc = GameObject(uiInterface, "grand_child", parent=c)
		self.assertEqual(c.getParent(), "game_area")
		self.assertEqual(gc.getParent(), c)
		self.assertTrue(c.inStackOf("game_area"))
		self.assertTrue(gc.inStackOf(c))
		self.assertTrue(gc.inStackOf("game_area"))
		self.assertFalse(c.inStackOf(gc))

	def _testMoveToNewParent(self):
		uiInterface = UIInterface()
		p1 = GameObject(uiInterface, "parent1", size=(20, 20), childrenLayout=GridLayout((5, 5), (5, 5)))
		p2 = GameObject(uiInterface, "parent2", size=(50, 50), childrenLayout=FreeLayout())
		obj = GameObject(uiInterface, "obj1", size=(5, 5))
		self.assertEqual(obj.getLayoutPos(), ("auto", "auto"))
		# add child into grid
		self.assertEqual(p1.setChildAt((2, 1), obj), (True,None))
		self.assertTrue(p1.hasChild(obj))
		self.assertEqual(p1.getChildPlace(obj), (2, 1))
		self.assertEqual(obj.getLayoutPos(), (10, 5))
		self.assertEqual(obj.getEffectivePos(), (10, 5))
		# apply position offsetting 
		obj.setPos((2, 2))
		self.assertEqual(obj.getLayoutPos(), (10, 5))
		self.assertEqual(obj.getEffectivePos(), (12, 7))
		self.assertTrue(p1.hasChild(obj))
		# try to move to new parent just by using add (will not work)
		with self.assertRaises(ValueError) as context:
			p2.addChild(obj)
			self.assertTrue("parent" in context.exception)
		self.assertTrue(p1.hasChild(obj))
		self.assertFalse(p2.hasChild(obj))
		# move child to new parent using setParent (works)
		obj.setParent(p2)
		self.assertFalse(p1.hasChild(obj))
		self.assertTrue(p2.hasChild(obj))
		self.assertTrue(p2.hasChild(obj.getDivID()))
		self.assertFalse(p2.hasChild(obj.getDivID()+"foo"))
		self.assertEqual(p1.getChildPlace(obj), None)
		self.assertEqual(p1.getChildPlace(obj.getDivID()), None)
		self.assertEqual(p2.getChildPlace(obj), 0)
		self.assertEqual(p2.getChildPlace(obj.getDivID()), 0)
		self.assertEqual(obj.getLayoutPos(), ("auto", "auto"))
		# remove child by divID
		p2.removeChild(obj.getDivID())
		self.assertFalse(p2.hasChild(obj))
		
	def _testChangeParentBetweenTypes(self):
		uiInterface = UIInterface()
		p1 = GameObject(uiInterface, "parent1", size=(20, 20), childrenLayout=FreeLayout())
		pStr1 = "str_parent1"
		pStr2 = "str_parent2"
		obj = GameObject(uiInterface, "obj1", size=(5, 5))
		self.assertEqual(obj.getParent(), None)
		obj.setParent(pStr1)
		self.assertEqual(obj.getParent(), pStr1)
		obj.setParent(p1)
		self.assertEqual(obj.getParent(), p1)
		self.assertTrue(p1.hasChild(obj))
		obj.setParent(pStr1)
		self.assertEqual(obj.getParent(), pStr1)
		self.assertFalse(p1.hasChild(obj))
		obj.setParent(pStr2)
		self.assertEqual(obj.getParent(), pStr2)
		obj.setParent(None)
		self.assertEqual(obj.getParent(), None)
		obj.setParent(pStr1)
		self.assertEqual(obj.getParent(), pStr1)
		obj.setParent(None)
		self.assertEqual(obj.getParent(), None)
		obj.setParent(p1)
		self.assertEqual(obj.getParent(), p1)
		obj.setParent(None)
		self.assertEqual(obj.getParent(), None)

	def runTest(self):
		self._testFlags()
		self._testChildren()
		self._testGrandchild()
		self._testInitWithParent()
		self._testMoveToNewParent()
		self._testChangeParentBetweenTypes()
