import itertools
import flask

from pathlib import Path
from pathlib import PurePath

from .UIChangeInterface import UIChangeInterface


def flatten1(listOfLists):
    return [item for sublist in listOfLists for item in sublist]

def uiChangeReverse(uiState, uiChange):
	# TODO: UI Commands
	command = uiChange[0]
	'''
	if command == "list-add":
		return ["list-remove"] + stateChange[1:]
	if command == "var-set":
		varName = stateChange[1]
		if varName in state:
			return [command, varName, state[varName]]
		else:
			return ["remove", varName]
	'''
	
def applyUIChange(currentUIState, uiChange):
	# TODO: UI Commands
	command = uiChange[0]
	
# TODO, add something? center etc..?
uiStartState = {}


class BaseGame(UIChangeInterface):

	# TODO: part of the UI should be individual (secret to others)
	
	def __init__(self, name, gameRootPath: Path):
		self.name = name
		
		# One action per state
		self.actions = []
		self.gameStateHistory = [{}]
		self.uiStateHistory = [uiStartState]
		self.uiProgression = [[]] # How to go to from stateN to stateN+1
		self.uiRegression = [[],[]] # How to go from stateN to stateN-1
		
		self.gameRootPath = gameRootPath
		
		self.currentStateN = 0
		self.currentUIState = uiStartState
	
	# ----------------- Server Methods -----------------
		
	def getUIChanges(self, fromStateN, toStateN):
		fromStateN = max(fromStateN, 0)
		toStateN = min(toStateN, self.currentStateN)
		if fromStateN < toStateN:
			return flatten1(self.uiProgression[fromStateN:toStateN])
		elif fromStateN > toStateN:
			return flatten1(self.uiRegression[toStateN + 1:fromStateN + 1])
		else:
			return []
	
	def clientAction(self, actionObj):
		if self.actionAllowed(actionObj):
			# advance game state
			self.actions.append(actionObj)
			newState = self.performAction(actionObj)
			assert(newState)
			self.gameStateHistory.append(newState)
			self.currentStateN += 1
			# initiate next UI state tracking
			self.uiStateHistory.append(self.currentUIState)
			self.uiProgression.append([])
			self.uiRegression.append([])
			return True
		else:
			return False
			
	def startGame(self, players: list):
		assert(not self.hasStarted())
		actionObj = ["start_game", players]
		res = self.clientAction(actionObj)
		if not res:
			print("Error: Not allowed to start game, players:", players)
		return res
		
	def hasStarted(self):
		return self.currentStateN > 0
	
	# returns 'None' if path is forbidden
	def getFullPath(self, gameFile: PurePath):
		resPath = Path(self.gameRootPath, gameFile)
		if self.gameRootPath in resPath.parents:
			return resPath
		else:
			return None
	
	# ----------------- UI Methods -----------------
	
	def addUIChange(self, uiChange):
		currentStateN = self.currentStateN
		self.uiProgression[currentStateN].append(uiChange) # record the uiChange
		self.uiRegression[currentStateN + 1].insert(0, uiChangeReverse(self.currentUIState, uiChange)) # record the reverse uiChange
		applyUIChange(self.currentUIState, uiChange) # apply uiChange
		
	def addUIChanges(self, uiChanges: list):
		for uic in uiChanges:
			self.addUIChange(uic)
		