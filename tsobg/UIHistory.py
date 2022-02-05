from . import ui_state
from .ui_state import combineUIChanges, uiChangeReverse, applyUIChange


def flatten1(listOfLists):
	return [item for sublist in listOfLists for item in sublist]

def clamp(n, smallest, largest):
	return max(smallest, min(n, largest))

class UIHistory():

	def __init__(self):
		self.uiStateHistory = [ui_state.getUIStartState()]
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
		fromStateN = clamp(fromStateN, 0, currentStateN)
		toStateN = clamp(toStateN, 0, currentStateN)
		uiChanges = [("state_n", toStateN)]
		if fromStateN < toStateN:
			uiChanges += flatten1(self.uiProgressionHistory[fromStateN:toStateN])
		elif fromStateN > toStateN:
			uiChanges += flatten1(self.uiRegressionHistory[toStateN + 1:fromStateN + 1])
		else:
			pass
		return uiChanges

	def commitUIChanges(self):
		""" will create a new state from the working uiChanges and currentStateN increases by 1 """
		uiState = self.uiStateHistory[-1]
		progUIChanges = []
		regUIChanges = []
		for uiChange in self.stagedUIChanges:
			UIHistory.__applyUIChange(uiState, progUIChanges, regUIChanges, uiChange)
		self.uiStateHistory.append(uiState)
		self.uiProgressionHistory.append(progUIChanges)
		self.uiRegressionHistory.append(regUIChanges)
		self.stagedUIChanges = []

	def stageUIChange(self, uiChange):
		uiChange = ui_state.deAliasUIChange(uiChange);
		if len(self.stagedUIChanges) > 0:
			# try to combine with previous uiChange that was staged
			combUIChanges = ui_state.combineUIChanges(self.stagedUIChanges[-1], uiChange)
		else:
			combUIChanges = None
		if combUIChanges:
			self.stagedUIChanges[-1] = combUIChanges
		else:
			self.stagedUIChanges.append(uiChange)

	def __applyUIChange(uiState, progUIChanges, regUIChanges, uiChange):
		# prune uiChange
		uiChange = ui_state.pruneUIChange(uiState, uiChange)
		if uiChange == ("nop"):
			return
		# record the uiChange (prog and reg)
		progUIChanges.append(uiChange)
		regUIChanges.insert(0, uiChangeReverse(uiState, uiChange))
		# apply uiChange
		applyUIChange(uiState, uiChange)

	def discardUIChanges(self):
		self.workingUIState = self.uiStateHistory[-1]
		self.workingUIProgression = []
		self.workingUIRegression = []

	def revertTo(self, stateN):
		currentStateN = self.getCurrentStateN()
		if stateN > currentStateN:
			return False
		self.discardUIChanges()
		if stateN == currentStateN:
			return True
		self.workingUIState = self.uiStateHistory[stateN]
		self.uiStateHistory = self.uiStateHistory[0:stateN+1]
		self.uiProgressionHistory = self.uiProgressionHistory[0:stateN]
		self.uiRegressionHistory = self.uiRegressionHistory[0:stateN+1]
		return True
