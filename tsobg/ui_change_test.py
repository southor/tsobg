import unittest

from .BaseGame import pruneUIChange
from .BaseGame import uiChangeReverse
from .BaseGame import applyUIChange

class UIChange_test(unittest.TestCase):

	def createDivs():
		divs = {}
		divs["factory_space"] = {"parent":"center", "img":"factory.png"}
		divs["restaurant_space"] = {"parent":"center", "img":"restaurant.png"}
		return divs

	def testSetDivPrune(self, uiState, id, optsInput, optsExpected):
		prunedUIChange = pruneUIChange(uiState, ("set_div", id, optsInput))
		self.assertEqual(prunedUIChange, ("set_div", id, optsExpected))

	def testSetDivReverse(self, uiState, id, optsInput, optsExpected):
		uicReverse = uiChangeReverse(uiState, ("set_div", id, optsInput))
		self.assertEqual(uicReverse, ("set_div", id, optsExpected))

	def testSetDivApply(self, uiState, id, optsInput, uiStateExpected):
		applyUIChange(uiState,  ("set_div", id, optsInput))
		self.assertEqual(uiState, uiStateExpected)

	
		
		
	def testPrune(self):
		uiState = {"divs": UIChange_test.createDivs()}
		self.testSetDivPrune(uiState, "restaurant_space",	{"img":"restaurant.png"},	{})
		self.testSetDivPrune(uiState, "restaurant_space",	{"img":"food.png"},			{"img":"food.png"})
		self.testSetDivPrune(uiState, "plaza_space",		{"pos":"auto"},				{})
		
	def testReverse(self):
		uiState = {"divs": UIChange_test.createDivs()}
		self.testSetDivReverse(uiState, "factory_space",	{},										{})
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
					"workshop_space":  {"parent":"center", "img":"factory.png", "pos":(10, 10)}
					}
		self.testSetDivApply({"divs": divs1}, "workshop_space", {"parent":"center", "img":"workshop.png"}, {"divs":divs1}) # no actual changes
		self.testSetDivApply({"divs": divs1}, "workshop_space", {"parent":"center", "img":"factory.png", "pos":(10, 10)}, {"divs":divs2}) # two actual changes
		
	def runTest(self):
		self.testPrune()
		self.testReverse()
		self.testApply()
