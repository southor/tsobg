import itertools
import flask

from pathlib import Path
from pathlib import PurePath


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


class BaseGame:

	# TODO: part of the UI should be individual (secret to others)
	
	def __init__(self, name, gameRootPath: Path):
		self.name = name
		
		'''
		# One action per state
		self.actions = []
		self.gameStates = [{}]
		self.uiStates = [{}]
		self.uiChanges = [[]] # How to go to from stateN to stateN+1
		self.uiChangesReverse = [[],[]] # How to go from stateN to stateN-1
		'''
		
		# One action per state
		self.actions = []
		self.gameStateHistory = [{}]
		self.uiStateHistory = [uiStartState]
		self.uiProgression = [[]] # How to go to from stateN to stateN+1
		self.uiRegression = [[],[]] # How to go from stateN to stateN-1
		
		self.gameRootPath = gameRootPath
		
		self.currentStateN = 0
		self.currentUIState = uiStartState
	
	#def addStateChange(self, stateChange):
	#	self.stateChanges[currentStateN].append(stateChange)
		
	'''
	def applyUIChanges(state, uiChanges):
		for uic in uiChanges:
			# TODO: replace with ui commands
			command = uic[0]
			if command == "list-add":
				varName = uic[1]
				if varName not in state:
					state[varName] = []
				state[varName] += uic[2]
			if command == "list-remove":
				varName = uic[1]
				if varName not in state:
					state[varName] = []
				state[varName] += uic[2]
	'''
	
	
		
	'''
	def nextState(self):
		state = self.state
		stateChanges = self.stateChanges
		assert(len(stateChanges) == self.currentStateN + 1)
		assert(len(stateChangesReverse) == self.currentStateN + 1)
		# make state changes reverse
		stateChangesReverse.append([])
		for sc in reversed(stateChanges[self.currentStateN]):
			rsc = makeReverse(self.state, sc)
			stateChangesReverse[currentStateN + 1].append(rsc)
		# make state changes reverse	
		self.applyStateChanges(self.state, stateChanges[self.currentStateN])
		stateChanges.append([])
		self.currentStateN += 1
			
		assert(len(stateChanges) == self.currentStateN + 1)
		assert(len(stateChangesReverse) == self.currentStateN + 1)
	'''
	
	# ----------------- Server Methods -----------------
	
	
	'''
	def getCurrentUIState(self):
		return self.uiStates[self.currentStateN]
	'''
		
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
		'''
		actionObj = ["start_game", players]
		if self.actionAllowed(actionObj):
			# initiate first UI state tracking
			self.uiStates.append(self.uiStateStartup)
			self.uiChanges.append([])
			self.uiChangesReverse.append([])
			# TODO: correct?
			newState = self.performAction(actionObj)
			assert(newState)
			self.gameStates.append(newState)
		else:
			print("Error: Not allowed to start game, players:", players)
		'''
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
	
	'''
	def getGameRootPath(self):
		return self.gameRootPath
	'''
	
	# ----------------- Game Methods -----------------
	
	'''
	# URL for local game path (based on gameRootPath)
	def getURLFor(self, relPath):
		return flask.url_for("static", filename=relPath)
		#flask.url_for(localPath)
	'''
	
	def addUIChange(self, uiChange):
		currentStateN = self.currentStateN
		self.uiProgression[currentStateN].append(uiChange) # record the uiChange
		self.uiRegression[currentStateN + 1].insert(0, uiChangeReverse(self.currentUIState, uiChange)) # record the reverse uiChange
		applyUIChange(self.currentUIState, uiChange) # apply uiChange
		
	def addUIChanges(self, uiChanges: list):
		for uic in uiChanges:
			self.addUIChange(uic)
		