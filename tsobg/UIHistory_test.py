
import unittest

from .UIHistory import UIHistory

class UIHistory_test(unittest.TestCase):

	def runTest(self):
		uiHistory = UIHistory()
		self.assertEqual(len(uiHistory.uiProgressionHistory), 0)
		self.assertEqual(len(uiHistory.uiRegressionHistory), 1)
		# ui changes should get combined
		uiHistory.stageUIChange(("set_div", "factory", {"parent":"town"}))
		uiHistory.stageUIChange(("set_div", "factory", {"img":"purple_factory.png"}))
		self.assertEqual(len(uiHistory.stagedUIChanges), 1) # uiChanges should be combined
		# commit uiState1
		uiHistory.commitUIChanges()
		uiState1 = uiHistory.uiStateHistory[-1]
		# more changes
		uiHistory.stageUIChange(("set_div", "harbor", {"parent":"town"}))
		uiHistory.stageUIChange(("set_div", "factory", {"img":"pink_factory.png"}))
		# commit uiState2
		uiHistory.commitUIChanges()
		# more changes
		uiHistory.stageUIChange(("set_div", "harbor", {"img":"harbor.png"}))
		uiHistory.stageUIChange(("set_div", "harbor", {"pos":(10,10)}))
		uiHistory.stageUIChange(("set_div", "factory", {"pos":"auto"})) # change should be ignored
		uiHistory.stageUIChange(("set_div", "factory", {"img":"pink_factory.png"})) # change should be ignored
		# commit uiState3
		uiHistory.commitUIChanges()
		# commit uiState4 (with no additional changes)
		uiHistory.commitUIChanges()
		# test get uiChanges forward 1 step
		uiChanges = uiHistory.getUIChanges(1,2)
		self.assertEqual(uiChanges, [("state_n", 2),
									("set_div", "harbor", {"parent":"town"}),
									("set_div", "factory", {"img":"pink_factory.png"})])
		# test get uiChanges forward 2 steps
		uiChanges = uiHistory.getUIChanges(1,3)
		twoStepsExpected =  [("state_n", 3),
								("set_div", "harbor", {"parent":"town"}),
								("set_div", "factory", {"img":"pink_factory.png"}),
								("set_div", "harbor", {"img":"harbor.png", "left":10, "top":10})]
		self.assertEqual(uiChanges, twoStepsExpected)
		# test get uiChanges forward 3 steps
		uiChanges = uiHistory.getUIChanges(1,4)
		threeStepsExpected = [("state_n", 4)] + twoStepsExpected[1:]
		self.assertEqual(uiChanges, threeStepsExpected)
		# more changes
		uiHistory.stageUIChange(("set_div", "harbor", {"left":30}))
		# commit uiState5
		uiHistory.commitUIChanges()
		# test again uiChanges forward 3 steps
		uiChanges = uiHistory.getUIChanges(1,4)
		self.assertEqual(uiChanges, threeStepsExpected)
		# test uiChanges forward 4 steps
		uiChanges = uiHistory.getUIChanges(1,5)
		self.assertEqual(uiChanges, [("state_n", 5),
									("set_div", "harbor", {"parent":"town"}),
									("set_div", "factory", {"img":"pink_factory.png"}),
									("set_div", "harbor", {"img":"harbor.png", "left":10, "top":10}),
									("set_div", "harbor", {"left":30})])
		# test get uiChanges backward 1 steps
		uiChanges = uiHistory.getUIChanges(2,1)
		self.assertEqual(uiChanges, [("state_n", 1),
									("set_div", "factory", {"img":"purple_factory.png"}),
									("set_div", "harbor", {"parent":None})])
		
		
		# more changes
		uiHistory.stageUIChange(("set_div", "harbor", {"img":"marina.png"}))
		# revert to uiState1
		uiHistory.revertTo(1)
		# compare
		self.assertEqual(uiState1, uiHistory.uiStateHistory[-1])
		# check stateN
		self.assertEqual(uiHistory.getCurrentStateN(), 1)
		# check staged changes
		self.assertEqual(uiHistory.stagedUIChanges, [])
		# add new changes
		uiHistory.stageUIChange(("set_div", "harbor", {"parent":"island"}))
		# commit uiState2
		uiHistory.commitUIChanges()
		# test get uiChanges 2 steps
		uiChanges = uiHistory.getUIChanges(0,2)
		self.assertEqual(uiChanges, [("state_n",2),
									("set_div", "factory", {"parent":"town", "img":"purple_factory.png"}),
									("set_div", "harbor", {"parent":"island"})
									])