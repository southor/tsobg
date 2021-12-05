
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
		self.assertEqual(len(uiHistory.stagedUIChanges), 2)
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
		# test get uiChanges forward 1 step
		uiChanges = uiHistory.getUIChanges(1,2)
		self.assertEqual(uiChanges, [("state_n", 2),
									("set_div", "harbor", {"parent":"town"}),
									("set_div", "factory", {"img":"pink_factory.png"})])
		# test get uiChanges forward 2 steps
		uiChanges = uiHistory.getUIChanges(1,3)
		self.assertEqual(uiChanges, [("state_n", 3),
									("set_div", "harbor", {"parent":"town"}),
									("set_div", "factory", {"img":"pink_factory.png"}),
									("set_div", "harbor", {"img":"harbor.png", "pos":(10,10)})])
		# test get uiChanges backward 1 steps
		uiChanges = uiHistory.getUIChanges(2,1)
		self.assertEqual(uiChanges, [("state_n", 1),
									("set_div", "factory", {"img":"purple_factory.png"}),
									("set_div", "harbor", {"parent":None})])
		# revert
		uiHistory.revertTo(1)
		# compare
		self.assertEqual(uiState1, uiHistory.uiStateHistory[-1])