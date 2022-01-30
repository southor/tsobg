import unittest

from .GameLog import GameLog


class GameLog_test(unittest.TestCase):

	def runTest(self):
		gameLog = GameLog()

		gameLog.addLogEntry(0, "hello0")
		gameLog.addLogEntries(0, ["hello1", "hello2"])
		gameLog.addLogEntries(1, ["hello3"])

		self.assertEqual(gameLog.getLogEntries(0,1), [(0, 0, "hello0"), (1, 0, "hello1"), (2, 0, "hello2")])
		self.assertEqual(gameLog.getLogEntries(0,4), [(0, 0, "hello0"), (1, 0, "hello1"), (2, 0, "hello2"), (3, 1, "hello3")])
		self.assertEqual(gameLog.getLogEntries(2,3), [])
		self.assertEqual(gameLog.getLogEntries(0,0), [])
		self.assertEqual(gameLog.getLogEntries(1,1), [])

		gameLog.addLogEntries(2, ["hello4", "hello5"])

		self.assertEqual(gameLog._GameLog__findStateBeginIdx(1), 3)
		self.assertEqual(gameLog._GameLog__findStateEndIdx(1), 4)
		self.assertEqual(gameLog._GameLog__findStateBeginIdx(0), 0)
		self.assertEqual(gameLog._GameLog__findStateEndIdx(2), 6)

		self.assertEqual(gameLog.getLogEntries(0,1), [(0, 0, "hello0"), (1, 0, "hello1"), (2, 0, "hello2")])
		self.assertEqual(gameLog.getLogEntries(0,4), [(0, 0, "hello0"), (1, 0, "hello1"), (2, 0, "hello2"), (3, 1, "hello3"), (4, 2, "hello4"), (5, 2, "hello5")])
		self.assertEqual(gameLog.getLogEntries(2,3), [(4, 2, "hello4"), (5, 2, "hello5")])
		self.assertEqual(gameLog.getLogEntries(0,0), [])
		self.assertEqual(gameLog.getLogEntries(1,1), [])

		self.assertRaises(RuntimeError, gameLog.addLogEntry, 0, "foo") # currentStateN=0 is not consistent with earlier added stateN=2
		self.assertRaises(RuntimeError, gameLog.addLogEntry, 1, "bar") # currentStateN=1 is not consistent with earlier added stateN=2

		gameLog.clearLogEntries(1)

		self.assertEqual(gameLog.getLogEntries(0,1), [(0, 0, "hello0"), (1, 0, "hello1"), (2, 0, "hello2")])
		self.assertEqual(gameLog.getLogEntries(0,4), [(0, 0, "hello0"), (1, 0, "hello1"), (2, 0, "hello2")])
		self.assertEqual(gameLog.getLogEntries(2,3), [])
		self.assertEqual(gameLog.getLogEntries(0,0), [])
		self.assertEqual(gameLog.getLogEntries(1,1), [])

		
