import unittest


import sys
from pathlib import Path
pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere / "Skyscrapers"))

from MainBoard_test import MainBoard_test

suite = unittest.TestSuite()
suite.addTest(MainBoard_test())

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
