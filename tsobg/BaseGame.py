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
		self.playerUIHistories = {} # later add one UIHistory object per player
		self.currentStateN = 0
	
	# ----------------- Server Methods -----------------
	
	def getUIChanges(self, playerId, fromStateN, toStateN):
		if self.hasStarted():
			if playerId in self.playerUIHistories:
				assert(self.playerUIHistories[playerId].getCurrentStateN() == self.currentStateN)
				return self.playerUIHistories[playerId].getUIChanges(fromStateN, toStateN)
			else:
				print("Call to getUIChanges with invalid playerId: {}, fromStateN={}, toStateN={}.format(playerId, fromStateN, toStateN")
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
			for uiHistory in self.playerUIHistories.values():
				uiHistory.commitUIChanges()
			return True
		else:
			return False
			
	def startGame(self, playerIDs: list):
		assert(not self.hasStarted())
		for p in playerIDs:
			self.playerUIHistories[p] = UIHistory()
		actionObj = ["start_game", playerIDs]
		res = self.clientAction(actionObj)
		if not res:
			print("Error: Not allowed to start game, playerIDs:", playerIDs)
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
	
	def stageUIChange_OnePlayer(self, playerID, uiChange):
		self.playerUIHistories[playerID].stageUIChange(uiChange)
	
	def stageUIChange_SomePlayers(self, playerIDs, uiChange):
		for p in playerIDs:
			self.playerUIHistories[p].stageUIChange(uiChange)

	def stageUIChange_AllPlayers(self, uiChange):
		for uiHistory in self.playerUIHistories.values():
			uiHistory.stageUIChange(uiChange)

	def stageUIChanges_OnePlayer(self, playerIDs, uiChanges: list):
		for uiChange in uiChanges:
			self.playerUIHistories[playerID].stageUIChange(uiChange)
	
	def stageUIChanges_SomePlayers(self, playerIDs, uiChanges: list):
		for uiChange in uiChanges:
			for p in playerIDs:
				self.playerUIHistories[p].stageUIChange(uiChange)
		
	def stageUIChanges_AllPlayers(self, uiChanges: list):
		for uiChange in uiChanges:
			for uiHistory in self.playerUIHistories.values():
				uiHistory.stageUIChange(uiChange)
		