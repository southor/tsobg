import unittest

from .ui_state import combineUIChanges, pruneUIChange, uiChangeReverse, applyUIChange


class UIState_test(unittest.TestCase):

	def createDivs():
		divs = {}
		divs["factory_space"] = {"parent":"center", "img":"factory.png"}
		divs["restaurant_space"] = {"parent":"center", "img":"restaurant.png"}
		return divs

	def testSizeToCSSpxComponents(size):
		pass # todo

	def testDeAliasUIChange(self):
		pass # todo

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

	def testSetDivApply(self, uiState, id, optsInput, uiStateExpected):
		applyUIChange(uiState,  ("set_div", id, optsInput))
		self.assertEqual(uiState, uiStateExpected)
	
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
