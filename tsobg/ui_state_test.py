import unittest
from copy import deepcopy

from .ui_state import sizeToCSSpxComponents, deAliasUIChange, combineUIChanges, pruneUIChange, uiChangeReverse, applyUIChange


class UIState_test(unittest.TestCase):

	def createDivs():
		divs = {}
		divs["factory_space"] = {"parent":"center", "img":"factory.png"}
		divs["restaurant_space"] = {"parent":"center", "img":"restaurant.png"}
		return divs

	def testSizeToCSSpxComponents(self):
		self.assertEqual(sizeToCSSpxComponents("auto"), ("auto", "auto"))
		self.assertEqual(sizeToCSSpxComponents(("auto", "auto")), ("auto", "auto"))
		self.assertEqual(sizeToCSSpxComponents((5, "auto")), ("5px", "auto"))
		self.assertEqual(sizeToCSSpxComponents(("auto", 10)), ("auto", "10px"))
		self.assertEqual(sizeToCSSpxComponents((5, 10)), ("5px", "10px"))
		self.assertEqual(sizeToCSSpxComponents([5, "auto"]), ("5px", "10px")) # list should also work

	def testDeAliasUIChange(self):
		uiChange1 = ("set_div", "foo_div", {"parent":"bar_div", "pos":(10, 20)})
		uiChange2 = ("set_div", "foo_div", {"color":"red", "size":(30, 40)})
		uiChange3 = ("set_div", "foo_div", {"parent":"bar_div", "color":"blue"})
		combUIChange = combineUIChanges(uiChange1, uiChange2)
		daUIChange1 = deAliasUIChange(uiChange1)
		daUIChange2 = deAliasUIChange(uiChange2)
		daUIChange3 = deAliasUIChange(uiChange3)
		daUIChangeComb = deAliasUIChange(combUIChange)
		self.assertFalse(uiChange1 is daUIChange1) # should not be the same object
		self.assertFalse(uiChange2 is daUIChange2) # should not be the same object
		self.assertFalse(uiChange3 is daUIChange3) # should be the same object (since no alias exists)
		self.assertEqual(daUIChange1, ("set_div", "foo_div", {"parent":"bar_div", "left":"10px", "top":"20px"}))
		self.assertEqual(daUIChange2, ("set_div", "foo_div", {"color":"red", "width":"30px", "height":"40px"}))
		self.assertEqual(daUIChange3, ("set_div", "foo_div", {"parent":"bar_div", "color":"blue"}))
		self.assertEqual(combUIChange, ("set_div", "foo_div", {"parent":"bar_div", "color":"red", "left":"10px", "top":"20px", "width":"30px", "height":"40px"}))


	def testSetDivPrune(self, uiState, id, optsInput, optsExpected = None):
		prunedUIChange = pruneUIChange(uiState, ("set_div", id, optsInput))
		if optsExpected == None:
			self.assertEqual(prunedUIChange, ("nop"))
		else:
			self.assertEqual(prunedUIChange, ("set_div", id, optsExpected))

	def testSetDivReverse(self, uiState, id, optsInput, optsExpected = None):
		uicReverse = uiChangeReverse(uiState, ("set_div", id, optsInput))
		if optsExpected == None:
			self.assertEqual(uicReverse, ("nop"))
		else:
			self.assertEqual(uicReverse, ("set_div", id, optsExpected))

	def testSetDivApply(self, uiStateOriginal, id, optsInput, uiStateExpected):
		uiState = deepcopy(uiStateOriginal)
		modifiedUIState = applyUIChange(uiState,  ("set_div", id, optsInput))
		self.assertEqual(modifiedUIState, uiStateExpected) # test expected changes
		self.assertEqual(uiState, uiStateOriginal) # test original not modified
		self.assertTrue((modifiedUIState is not uiState) or (uiStateOriginal == uiStateExpected)) # modifiedState should be a new object unless...
	
	def testCombine(self):
		uic = ("set_div", "homer", {"left":"45px", "top":"10px"})
		uicOriginal = uic.copy()
		# command mismatch, should not combine
		res = combineUIChange(uic, ("some_command", "homer", {"left":20}))
		self.assertFalse(res)
		# id mismatch, should not combine
		res = combineUIChange(uic, ("set_div", "bart", {"left":20}))
		self.assertFalse(res)
		# command,id match, should combine (but original unchanged)
		res = combineUIChange(uic, ("set_div", "homer", {"left":20}))
		self.assertTrue(res)
		self.assertEqual(res[2], {"left":10, "top":5})
		self.assertEqual(uic, uicOriginal)
		
	def testPrune(self):
		uiState = {"divs": UIState_test.createDivs()}
		self.testSetDivPrune(uiState, "restaurant_space",	{"img":"restaurant.png"}) # expecting nop
		self.testSetDivPrune(uiState, "restaurant_space",	{"left":"auto"}) # expecting nop
		self.testSetDivPrune(uiState, "restaurant_space",	{"img":"food.png"},			{"img":"food.png"})
		self.testSetDivPrune(uiState, "plaza_space",		{"left":"auto"}) # expecting nop
		
	def testReverse(self):
		uiState = {"divs": UIState_test.createDivs()}
		self.testSetDivReverse(uiState, "factory_space",	{}) # expecting nop
		self.testSetDivReverse(uiState, "factory_space",	{"parent":"street"},					{"parent":"center"})
		self.testSetDivReverse(uiState, "restaurant_space",	{"img":"restaurant.png"},				{"img":"restaurant.png"})
		self.testSetDivReverse(uiState, "restaurant_space",	{"img":"food.png"},						{"img":"restaurant.png"})
		self.testSetDivReverse(uiState, "plaza_space",		{"img":"plaza.png"},					{"img":None})
		self.testSetDivReverse(uiState, "plaza_space",		{"img":"plaza.png", "parent":"center"},	{"img":None, "parent":None})

	def testApply(self):
		divs1 = {
					"factory_space":  {"parent":"center", "img":"factory.png"},
					"workshop_space":  {"parent":"center", "img":"workshop.png"}
					}
		divs2 = {
					"factory_space":  {"parent":"center", "img":"factory.png"},
					"workshop_space":  {"parent":"center", "img":"factory.png", "left":10, "top":10}
					}
		self.testSetDivApply({"divs": divs1}, "workshop_space", {"parent":"center", "img":"workshop.png"}, {"divs":divs1}) # no actual changes
		self.testSetDivApply({"divs": divs1}, "workshop_space", {"parent":"center", "img":"factory.png", "left":10, "top":10}, {"divs":divs2}) # two actual changes
		
	def runTest(self):
		self.testPrune()
		self.testReverse()
		self.testApply()
