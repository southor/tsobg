import itertools
import flask

from pathlib import Path
from pathlib import PurePath

from .UIChangeInterface import UIChangeInterface
from .UIHistory import UIHistory


class BaseGame(UIChangeInterface):

	# TODO: part of the UI should be individual (secret to others)
	
	def __init__(self, name, gameRootPath: Path):
		self.name = name
		self.gameRootPath = gameRootPath
		# One action per state
		self.actions = []
		self.gameStateHistory = [{}]
		self.uiStateHistory = UIHistory()
		self.currentStateN = 0
	
	# ----------------- Server Methods -----------------
		
	def getUIChanges(self, fromStateN, toStateN):
		assert(self.uiStateHistory.currentStateN == self.currentStateN)
		return self.uiStateHistory.getUIChanges(fromStateN, toStateN)
	
	def clientAction(self, actionObj):
		if self.actionAllowed(actionObj):
			# advance game state
			self.actions.append(actionObj)
			newState = self.performAction(actionObj)
			assert(newState)
			self.gameStateHistory.append(newState)
			self.currentStateN += 1
			self.uiStateHistory.initNext()
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
		uiChange = self.uiStateHistory.pruneUIChange(uiChange)
		self.uiStateHistory.addUIChange(uiChange)
		
	def addUIChanges(self, uiChanges: list):
		for uic in uiChanges:
			self.addUIChange(uic)
		