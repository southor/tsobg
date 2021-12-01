from . import ui_state
from .ui_state import uiChangeReverse, applyUIChange


def flatten1(listOfLists):
	return [item for sublist in listOfLists for item in sublist]

def clamp(n, smallest, largest):
	return max(smallest, min(n, largest))

class UIHistory():

	def __init__(self):
		self.uiStateHistory = [ui_state.uiStartState]
		self.uiProgression = [[]] # How to go to from stateN to stateN+1
		self.uiRegression = [[],[]] # How to go from stateN to stateN-1
		self.currentStateN = 0
		self.currentUIState = ui_state.uiStartState

	def getUIChanges(self, fromStateN, toStateN):
		fromStateN = clamp(fromStateN, 0, self.currentStateN)
		toStateN = clamp(toStateN, 0, self.currentStateN)
		uiChanges = [("state_n", toStateN)] 
		if fromStateN < toStateN:
			uiChanges += flatten1(self.uiProgression[fromStateN:toStateN])
		elif fromStateN > toStateN:
			uiChanges += flatten1(self.uiRegression[toStateN + 1:fromStateN + 1])
		else:
			pass
		return uiChanges

	def initNext(self):
		self.currentStateN += 1
		self.uiStateHistory.append(self.currentUIState)
		self.uiProgression.append([])
		self.uiRegression.append([])

	def pruneUIChange(self, uiChange):
		return ui_state.pruneUIChange(self.currentUIState, uiChange)

	def addUIChange(self, uiChange):
		currentStateN = self.currentStateN
		self.uiProgression[currentStateN].append(uiChange) # record the uiChange
		self.uiRegression[currentStateN + 1].insert(0, uiChangeReverse(self.currentUIState, uiChange)) # record the reverse uiChange
		applyUIChange(self.currentUIState, uiChange) # apply uiChange
