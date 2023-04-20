
import unittest

from .UIInterface import UIInterface
from .GameObject import GameObject
from .FreeLayout import FreeLayout
from .GridLayout import GridLayout


class GameObject_test(unittest.TestCase):
	
	# def testFlags(self):
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
		
	def testFlags(self):
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

	def testGrandchild(self):
		# test: FreeLayout, FreeLayout
		p = GameObject(UIInterface(), "parent", size=(20, 20))
		c = GameObject(UIInterface(), "child", parent=p, pos=(5, 0), size=(10, 10))
		gc = GameObject(UIInterface(), "grandchild", size=(5, 5))
		c.putObject(gc, (3, 0))
		self.assertEqual(p.getLayoutType(), FreeLayout)
		self.assertEqual(c.getLayoutType(), FreeLayout)
		self.assertEqual(gc.getLayoutType(), FreeLayout)
		self.assertEqual(c.getParent(), p)
		self.assertEqual(gc.getParent(), c)
		self.assertTrue(p.hasObject(c, False))
		self.assertTrue(p.hasObject(gc, True))
		self.assertFalse(p.hasObject(gc, False))
		self.assertEqual(c.getObjectLayoutArgs(gc), (3, 0))
		self.assertEqual(p.getObjectLayoutArgs(c), (5, 0))
		self.assertEqual(p.getObjectLayoutArgs(gc), None) # Without recursive, grand child should not be found
		self.assertEqual(p.getObjectLayoutArgs(gc, True), (5, 0)) # With recursive, grand child is found, coordinate of child should be returned
		# test: TileLayout, FreeLayout
		p.removeObject(c)
		self.assertEqual(c.getParent(), None)
		layout = GridLayout((5, 5), (20, 20))
		p = GameObject(UIInterface(), "parent", layout=layout, size=(100, 100))
		p.putObject(c, 0, 2)
		self.assertEqual(p.getLayoutType(), GridLayout)
		self.assertEqual(c.getLayoutType(), FreeLayout)
		self.assertEqual(gc.getLayoutType(), FreeLayout)
		self.assertTrue(p.hasObject(gc, True))
		self.assertFalse(p.hasObject(gc, False))
		self.assertEqual(c.getObjectLayoutArgs(gc), (3, 0))
		self.assertEqual(p.getObjectLayoutArgs(c), (0, 2))
		self.assertEqual(p.getObjectLayoutArgs(gc), None) # Without recursive, grand child should not be found
		self.assertEqual(p.getObjectLayoutArgs(gc, True), (0, 2)) # With recursive, grand child is found, coordinate of child should be returned
		self.assertEqual(c.getPos(), (0, 40)) # pos of child should have been set by GridLayout (grid pos multiplied by tile size)

	def runTest(self):
		self.testFlags()
		self.testGrandchild()
