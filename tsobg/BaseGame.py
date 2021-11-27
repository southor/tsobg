import itertools
import flask

from pathlib import Path
from pathlib import PurePath

from .UIChangeInterface import UIChangeInterface


def flatten1(listOfLists):
    return [item for sublist in listOfLists for item in sublist]

divOptsDefaults = {"parent":None, "pos":"auto", "size":"auto", "img":None, "border":None, "color":"transparent"}

# returns pruned uiChange 
def pruneUIChange(uiState, uiChange):
	stateDivs = uiState["divs"]
	command = uiChange[0]
	if command == "set_div":
		id = uiChange[1]
		opts = uiChange[2]
		divState = stateDivs.get(id, {})
		prunedOpts = {}
		for key,value in opts.items():
			valueState = divState.get(key, divOptsDefaults[key])
			if value != valueState:
				prunedOpts[key] = value
		return ("set_div", id, prunedOpts)
	else:
		raise RuntimeException("Unknown command: " + command)

# returns reversed version of uiChange 
def uiChangeReverse(uiState, uiChange):
	stateDivs = uiState["divs"]
	command = uiChange[0]
	if command == "set_div":
		id = uiChange[1]
		opts = uiChange[2]
		divState = stateDivs.get(id, {})
		revOpts = {}
		for key,value in opts.items():
			if key in divState:
				revOpts[key] = divState[key]
			else:
				revOpts[key] = divOptsDefaults[key]
		return ("set_div", id, revOpts)
	else:
		raise RuntimeException("Unknown command: " + command)
	
# modifies uiState with uiChange
def applyUIChange(uiState, uiChange):
	stateDivs = uiState["divs"]
	command = uiChange[0]
	if command == "set_div":
		id = uiChange[1]
		opts = uiChange[2]
		if id not in stateDivs:
			stateDivs[id] = opts
		else:
			stateDivs[id].update(opts)
	else:
		raise RuntimeException("Unknown command: " + command)
	


uiStartState = { "divs": {} }


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
		uiChanges = [("state_n", toStateN)]
		if fromStateN < toStateN:
			uiChanges += flatten1(self.uiProgression[fromStateN:toStateN])
		elif fromStateN > toStateN:
			uiChanges += flatten1(self.uiRegression[toStateN + 1:fromStateN + 1])
		else:
			pass
		return uiChanges
	
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
		uiChange = pruneUIChange(self.currentUIState, uiChange)
		currentStateN = self.currentStateN
		self.uiProgression[currentStateN].append(uiChange) # record the uiChange
		self.uiRegression[currentStateN + 1].insert(0, uiChangeReverse(self.currentUIState, uiChange)) # record the reverse uiChange
		applyUIChange(self.currentUIState, uiChange) # apply uiChange
		
	def addUIChanges(self, uiChanges: list):
		for uic in uiChanges:
			self.addUIChange(uic)
		