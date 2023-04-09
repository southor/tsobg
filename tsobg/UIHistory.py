from .UIState import UIState
from .UIState import combineUIChanges

def flatten1(listOfLists):
	return [item for sublist in listOfLists for item in sublist]


class UIHistory():

	def __init__(self):
		self.uiStateHistory = [UIState()]
		self.uiProgressionHistory = [] # member [0] tells how to go from stateN=0 to stateN=1
		self.uiRegressionHistory = [[]] # member [1] tells how to go from stateN=1 to stateN=0
		self.stagedUIChanges = []
		
	def getNStates(self):
		return len(self.uiStateHistory)

	def getCurrentStateN(self):
		return len(self.uiStateHistory) - 1

	def getNextStateN(self):
		return len(self.uiStateHistory)

	def getUIChanges(self, fromStateN, toStateN):
		currentStateN = self.getCurrentStateN()
		assert(fromStateN >= 0 and fromStateN <= currentStateN)
		assert(toStateN >= 0 and toStateN <= currentStateN)
		if fromStateN < toStateN:
			return flatten1(self.uiProgressionHistory[fromStateN:toStateN])
		elif fromStateN > toStateN:
			return flatten1(self.uiRegressionHistory[toStateN + 1:fromStateN + 1])
		else:
			return []

	def commitUIChanges(self):
		""" will create a new state from the working uiChanges and currentStateN increases by 1 """
		uiState = self.uiStateHistory[-1]
		progUIChanges = []
		regUIChanges = []
		for uiChange in self.stagedUIChanges:
			uiState = UIHistory._applyUIChange(uiState, progUIChanges, regUIChanges, uiChange)
		self.uiStateHistory.append(uiState)
		self.uiProgressionHistory.append(progUIChanges)
		self.uiRegressionHistory.append(regUIChanges)
		self.stagedUIChanges = []

	def stageUIChange(self, uiChange):
		""" uiChange must be free of aliases """
		if len(self.stagedUIChanges) > 0:
			# try to combine with previous uiChange that was staged
			combUIChanges = combineUIChanges(self.stagedUIChanges[-1], uiChange)
		else:
			combUIChanges = None
		if combUIChanges:
			self.stagedUIChanges[-1] = combUIChanges
		else:
			self.stagedUIChanges.append(uiChange)

	def _applyUIChange(uiState, progUIChanges, regUIChanges, uiChange):
		""" returns the modified uiState """
		# prune uiChange
		uiChange = uiState.pruneUIChange(uiChange)
		if uiChange == ("nop"):
			return uiState
		# record the uiChange (prog and reg)
		progUIChanges.append(uiChange)
		regUIChanges.insert(0, uiState.uiChangeReverse(uiChange))
		# apply uiChange
		return uiState.applyUIChange(uiChange)

	def revertTo(self, stateN):
		assert(stateN >= 0)
		currentStateN = self.getCurrentStateN()
		if stateN > currentStateN:
			return False
		self.stagedUIChanges = []
		if stateN == currentStateN:
			return True
		self.uiStateHistory = self.uiStateHistory[0:stateN+1]
		self.uiProgressionHistory = self.uiProgressionHistory[0:stateN]
		self.uiRegressionHistory = self.uiRegressionHistory[0:stateN+1]
		return True
