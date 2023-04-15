
import unittest

from .UIInterface import UIInterface
from .GameObject import GameObject


class GameObject_test(unittest.TestCase):
	
	def testFlags(self):
		go = GameObject(UIInterface(), "testobj")
		# test default flag values
		self.assertTrue(go.getFlag("visible"))
		self.assertTrue(go.getFlag("trapClicks"))
		self.assertFalse(go.getFlag("selectable"))
		self.assertEqual(go.getFlags(), {"visible", "trapClicks"})
		# test modify flag values
		go.setFlags("selectable")
		self.assertEqual(go.getFlags(), {"visible", "trapClicks", "selectable"})
		go.setFlags({"selectable"})
		self.assertEqual(go.getFlags(), {"selectable"})
		go.setFlags("visible")
		self.assertEqual(go.getFlags(), {"visible", "selectable"})
		go.setFlags(visible=False)
		self.assertEqual(go.getFlags(), {"selectable"})
		go.setFlags({"trapClicks"}, trapClicks=False)
		self.assertEqual(go.getFlags(), set())
		# Reset to new GameObject, test more modify flag values
		go = GameObject(UIInterface(), "testobj")
		self.assertEqual(go.getFlags(), {"visible", "trapClicks"})
		go.setFlags(set(), "trapClicks", "visible", trapClicks=False)
		self.assertEqual(go.getFlags(), {"visible"})
		go.setFlags({"visible", "selectable"}, {"selectable":False})
		self.assertEqual(go.getFlags(), {"visible"})
		go.setFlags({"visible", "selectable"}, {"selectable":False}, "selectable")
		self.assertEqual(go.getFlags(), {"visible", "selectable"})

	def runTest(self):
		self.testFlags()
