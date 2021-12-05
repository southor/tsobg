from . import ui_state
from .ui_state import updateUIChange, uiChangeReverse, applyUIChange


def flatten1(listOfLists):
	return [item for sublist in listOfLists for item in sublist]

def clamp(n, smallest, largest):
	return max(smallest, min(n, largest))

class UIHistory():

	def __init__(self):
		self.uiStateHistory = [ui_state.uiStartState]
		self.uiProgressionHistory = [] # member [0] tells how to go from stateN=0 to stateN=1
		self.uiRegressionHistory = [[]] # member [1] tells how to go from stateN=1 to stateN=0
		self.workingUIState = ui_state.uiStartState
		self.workingUIProgression = []
		self.workingUIRegression = []
		
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
		self.uiStateHistory.append(self.workingUIState)
		self.uiProgressionHistory.append(self.workingUIProgression)
		self.uiRegressionHistory.append(self.workingUIRegression)
		self.workingUIProgression = []
		self.workingUIRegression = []

	def pruneUIChange(self, uiChange):
		return ui_state.pruneUIChange(self.workingUIState, uiChange)

	def stageUIChange(self, uiChange):
		progUIChanges = self.workingUIProgression
		regUIChanges = self.workingUIRegression
		# prune uiChange
		uiChange2 = self.pruneUIChange(uiChange)
		if uiChange2 == ("nop"):
			return
		assert(uiChange2[0] != "set_div" or uiChange2 is not uiChange) # if its a set_div then it must be a copy of the original
		uiChange = uiChange2
		# record the uiChange (update last or append)
		if len(progUIChanges) == 0 or not updateUIChange(progUIChanges[-1], uiChange):
			progUIChanges.append(uiChange)
		# record the reverse uiChange (update first or insert)
		uiChangeRev = uiChangeReverse(self.workingUIState, uiChange)
		if len(regUIChanges) > 0 and updateUIChange(uiChangeRev, regUIChanges[0]):
			regUIChanges[0] = uiChangeRev
		else:
			regUIChanges.insert(0, uiChangeRev)
		# apply uiChange
		applyUIChange(self.workingUIState, uiChange)

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
