import unittest
from copy import deepcopy

from .UIState import _sizeToWidthHeight, _deAliasUIChange, combineUIChanges
from .UIState import UIState



class UIState_test(unittest.TestCase):
	
	def createDivs():
		divs = {}
		divs["factory_space"] = {"parent":"center", "img":"factory.png"}
		divs["restaurant_space"] = {"parent":"center", "img":"restaurant.png"}
		return divs

	def _testSetDivPrune(self, uiState, id, optsInput, optsExpected = None):
		prunedUIChange = uiState.pruneUIChange(("set_div", id, optsInput))
		if optsExpected == None:
			self.assertEqual(prunedUIChange, ("nop"))
		else:
			self.assertEqual(prunedUIChange, ("set_div", id, optsExpected))

	def _testSetDivReverse(self, uiState, id, optsInput, optsExpected = None):
		uicReverse = uiState.uiChangeReverse(("set_div", id, optsInput))
		if optsExpected == None:
			self.assertEqual(uicReverse, ("nop"))
		else:
			self.assertEqual(uicReverse, ("set_div", id, optsExpected))

	def _testSetDivApply(self, uiStateOriginal, id, optsInput, uiStateExpected):
		uiState = deepcopy(uiStateOriginal)
		modifiedUIState = uiState.applyUIChange(("set_div", id, optsInput))
		self.assertEqual(modifiedUIState, uiStateExpected) # test expected changes
		self.assertEqual(uiState, uiStateOriginal) # test original not modified
		self.assertTrue((modifiedUIState is not uiState) or (uiStateOriginal == uiStateExpected)) # modifiedState should be a new object unless...

	def _testDeAliasUIChange(self, uiChange, daUIChangeExpected):
		daUIChange,isOriginal = _deAliasUIChange(uiChange)
		self.assertEqual(daUIChange, daUIChangeExpected)
		# should only be original if it did not change
		if (uiChange == daUIChange):
			self.assertTrue(isOriginal) 
		else:
			self.assertFalse(isOriginal)
	
	def testSizeToWidthHeight(self):
		self.assertEqual(_sizeToWidthHeight("auto"), ("auto", "auto"))
		self.assertEqual(_sizeToWidthHeight(("auto", "auto")), ("auto", "auto"))
		self.assertEqual(_sizeToWidthHeight(("auto", 10)), ("auto", 10))
		self.assertEqual(_sizeToWidthHeight((5, 10)), (5, 10))
		self.assertEqual(_sizeToWidthHeight((5, "auto")), (5, "auto"))
		self.assertEqual(_sizeToWidthHeight([5, "auto"]), (5, "auto")) # list should also work
		self.assertRaises(ValueError, _sizeToWidthHeight, *[5]) # wrong type
		self.assertRaises(ValueError, _sizeToWidthHeight, (5,)) # too few tuple members
		self.assertEqual(_sizeToWidthHeight((5,"auto", "auto")), (5, "auto")) # too many is ok
	
	def testDeAliasUIChange(self):
		uiChange1 = ("set_div", "foo_div", {"parent":"bar_div", "pos":(10, 20)})
		uiChange2 = ("set_div", "foo_div", {"color":"red", "size":(30, 40)})
		uiChange3 = ("set_max_n_div_selected", 2)
		uiChange4 = ("set_div", "foo_div", {"parent":"bar_div", "color":"blue"})
		combUIChange = combineUIChanges(uiChange1, uiChange2)
		daUIChangeComb,daUIChangeCombIsOriginal = _deAliasUIChange(combUIChange)
		self._testDeAliasUIChange(uiChange1, ("set_div", "foo_div", {"parent":"bar_div", "left":10, "top":20}))
		self._testDeAliasUIChange(uiChange2, ("set_div", "foo_div", {"color":"red", "width":30, "height":40}))
		self._testDeAliasUIChange(uiChange3, ("set_max_n_div_selected", 2))
		self._testDeAliasUIChange(uiChange4, ("set_div", "foo_div", {"parent":"bar_div", "color":"blue"}))
		self._testDeAliasUIChange(combUIChange, ("set_div", "foo_div", {"parent":"bar_div", "color":"red", "left":10, "top":20, "width":30, "height":40}))

	def testCombine(self):
		uic = ("set_div", "homer", {"left":"45px", "top":"10px"})
		# command mismatch, should not combine
		res = combineUIChanges(uic, ("some_command", "homer", {"left":20}))
		self.assertFalse(res)
		# id mismatch, should not combine
		res = combineUIChanges(uic, ("set_div", "bart", {"left":20}))
		self.assertFalse(res)
		# command,id match, should combine
		res = combineUIChanges(uic, ("set_div", "homer", {"left":20}))
		self.assertTrue(res)
		self.assertEqual(res[2], {"left":20, "top":"10px"})
		
	def testPrune(self):
		uiState = UIState(divs=UIState_test.createDivs())
		self._testSetDivPrune(uiState, "restaurant_space",	{"img":"restaurant.png"}) # expecting nop
		self._testSetDivPrune(uiState, "restaurant_space",	{"left":"auto"}) # expecting nop
		self._testSetDivPrune(uiState, "restaurant_space",	{"img":"food.png"},			{"img":"food.png"})
		self._testSetDivPrune(uiState, "plaza_space",		{"left":"auto"}) # expecting nop
	
	def testReverse(self):
		uiState = UIState(divs=UIState_test.createDivs())
		self._testSetDivReverse(uiState, "factory_space",	{"parent":"street"},					{"parent":"center"})
		self._testSetDivReverse(uiState, "factory_space",	{}) # expecting nop
		self._testSetDivReverse(uiState, "restaurant_space",	{"img":"restaurant.png"},				{"img":"restaurant.png"})
		self._testSetDivReverse(uiState, "restaurant_space",	{"img":"food.png"},						{"img":"restaurant.png"})
		self._testSetDivReverse(uiState, "plaza_space",		{"img":"plaza.png"},					{"img":None})
		self._testSetDivReverse(uiState, "plaza_space",		{"img":"plaza.png", "parent":"center"},	{"img":None, "parent":None})
		uiState.maxNDivSelected = 10
		self.assertEqual(uiState.uiChangeReverse(("set_max_num_div_selected", 2)), ("set_max_num_div_selected", 10))

	def testApply(self):
		divs1 = {
					"factory_space":  {"parent":"center", "img":"factory.png"},
					"workshop_space":  {"parent":"center", "img":"workshop.png"}
					}
		divs2 = {
					"factory_space":  {"parent":"center", "img":"factory.png"},
					"workshop_space":  {"parent":"center", "img":"factory.png", "left":"10px", "top":"10px"}
					}
		self._testSetDivApply(UIState(divs=divs1), "workshop_space", {"parent":"center", "img":"workshop.png"}, UIState(divs=divs1)) # no actual changes
		self._testSetDivApply(UIState(divs=divs1), "workshop_space", {"parent":"center", "img":"factory.png", "left":"10px", "top":"10px"}, UIState(divs=divs2)) # three actual changes
		uiState = UIState(divs=UIState_test.createDivs())
		uiState.maxNDivSelected = 10
		uiState.applyUIChange(("set_max_num_div_selected", 2))
		self.assertEqual(uiState.maxNDivSelected, 2)
	
	def runTest(self):
		self.testSizeToWidthHeight()
		self.testDeAliasUIChange()
		self.testCombine()
		self.testPrune()
		self.testReverse()
		self.testApply()
