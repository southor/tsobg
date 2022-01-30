# Runs all tests in python module "tsobg":
# python3 tests.py


import unittest

from tsobg.ui_state_test import UIState_test
from tsobg.Deck_test import Deck_test
from tsobg.UIGrid_test import UIGrid_test
from tsobg.UIHistory_test import UIHistory_test
from tsobg.GameLog_test import GameLog_test


suite = unittest.TestSuite()
suite.addTest(UIState_test())
suite.addTest(Deck_test())
suite.addTest(UIGrid_test())
suite.addTest(UIHistory_test())
suite.addTest(GameLog_test())


result = unittest.TestResult()
suite.run(result)

if result.failures or result.errors:
	for f in result.failures:
		print("------------")
		print("Fail in: " + str(f[0]))
		print(f[1].replace('\\n', '\n'))
	for e in result.errors:
		print("------------")
		print("Error in: " + str(e[0]))
		print(e[1].replace('\\n', '\n'))
else:
	print("all tests ok")

