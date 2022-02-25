import itertools
import flask

from pathlib import Path
from pathlib import PurePath

from .UIInterface import UIInterface
from .UIHistory import UIHistory
from .GameLog import GameLog
from .UIState import deAliasUIChange

class GameManager(UIInterface):
	
	def __init__(self):
	#def __init__(self, name, gameRootPath: Path):
		#self.name = name
		#self.gameRootPath = gameRootPath
		self.actionHistory = [] # A list of tuples (playerId, actionObj)
		self.playerUIHistories = {} # map from playerId to UIHistory object
		self.currentRevertN = 0
		self.currentStateN = 0
		self.gameLog = GameLog() # game log entries shared by players
		self.clientMsgs = {} # instant messages waiting to be sent to players

	# ----------------- Help Methods -----------------

	def __clampNumber(n, smallest, largest):
		return max(smallest, min(n, largest))
	
	def __popClientMessages(self, playerId):
		msgEntries = self.clientMsgs.get(playerId, [])
		if msgEntries:
			self.clientMsgs[playerId] = []
		return [("msg",) + m for m in msgEntries]

	def __getLogEntries(self, fromStateN, toStateN):
		logEntries = self.gameLog.getLogEntries(fromStateN, toStateN)
		return [("game_log",) + l for l in logEntries]

	def __getUIChanges(self, playerId, fromStateN, toStateN):
		if self.gameStarted():
			if playerId in self.playerUIHistories:
				assert(self.playerUIHistories[playerId].getCurrentStateN() == self.currentStateN)
				return self.playerUIHistories[playerId].getUIChanges(fromStateN, toStateN)
			else:
				print("Call to getUIChanges with invalid playerId: {}, fromStateN={}, toStateN={}.format(playerId, fromStateN, toStateN")
		else:
			return []
	
	# ----------------- Server Methods -----------------
	
	def getGame(self):
		return self.game

	def setGame(self, game):
		""" should only be called once """
		assert(not hasattr(self, 'game'))
		self.game = game

	def getClientUpdates(self, playerId, revertN, fromStateN, toStateN):
		fromStateN = GameManager.__clampNumber(fromStateN, 0, self.currentStateN)
		toStateN = GameManager.__clampNumber(toStateN, 0, self.currentStateN)
		data = []
		if revertN != self.currentRevertN:
			# we reset the client and let it recreate divs and log from stateN zero
			data += [("reset_ui",), ("revert_n", self.currentRevertN)]
			fromStateN = 0
		data += [("state_n", toStateN)]
		data += self.__popClientMessages(playerId)
		if self.gameStarted():
			data += self.__getLogEntries(fromStateN, toStateN)
			data += self.__getUIChanges(playerId, fromStateN, toStateN)
		return data
	
	def clientAction(self, currentRevertN, stateN, actionObj, playerId = None):
		if stateN != self.currentStateN:
			return False # TODO: respond 409 conflict?
		if self.game.actionAllowed(actionObj, playerId=playerId):
			# advance game state
			self.actionHistory.append((playerId, actionObj))
			self.game.performAction(actionObj, playerId=playerId)
			self.currentStateN += 1
			for uiHistory in self.playerUIHistories.values():
				uiHistory.commitUIChanges()
			return True
		else:
			return False
			
	def startGame(self, playerIDs: list, playerNames: list):
		assert(not self.gameStarted())
		assert(self.currentRevertN == 0)
		for p in playerIDs:
			self.playerUIHistories[p] = UIHistory()
			self.clientMsgs[p] = []
		actionObj = ("start_game", playerIDs, playerNames)
		res = self.clientAction(0, 0, actionObj)
		if res:
			print("Game started, playerIDs:", playerIDs)
		else:
			print("Error: Not allowed to start game, playerIDs:", playerIDs)
		return res
		
	def gameStarted(self):
		return self.currentStateN > 0

	def revertToStateN(self, stateN):
		toStateN = GameManager.__clampNumber(stateN, 1, self.currentStateN)
		if toStateN < self.currentStateN:
			# revert game state
			# go back to game state zero, and rebuild everything from there
			fromStateN = self.currentStateN
			self.gameLog.clearLogEntries(0)
			actionsToReplay = self.actionHistory[0:stateN]
			self.actionHistory = []
			self.game.resetGameState()
			self.currentRevertN += 1
			self.currentStateN = 0
			for uiHistory in self.playerUIHistories.values():
				uiHistory.revertTo(0)
			for playerId,actionObj in actionsToReplay:
				self.clientAction(self.currentRevertN, self.currentStateN, actionObj, playerId = playerId)
			msg = "Reverted from game state {} to {}".format(fromStateN, toStateN)
			print(msg)
			self.sendMessageToPlayers(msg)
			return msg
		else:
			return "No revert happened (stateN {} is not smaller than current {})".format(stateN, self.currentStateN)
	
	# returns 'None' if path is forbidden
	def getFullPath(self, gameFile: PurePath):
		resPath = Path(self.game.getRootPath(), gameFile)
		if self.game.getRootPath() in resPath.parents:
			return resPath
		else:
			return None
	
	# ----------------- Client Message methods -----------------
	
	def sendMessageToPlayer(self, msgEntry, playerID):
		""" msgEntry: tuple (level, text) or just text """
		if isinstance(msgEntry, str):
			msgEntry = ("info", msgEntry)
		self.clientMsgs[playerID].append(msgEntry)

	def sendMessageToPlayers(self, msgEntry, playerIDs = None):
		""" msgEntry: tuple (level, text) or just text """
		if isinstance(msgEntry, str):
			msgEntry = ("info", msgEntry)
		if not playerIDs:
			playerIDs = self.clientMsgs.keys() # get all players
		for p in playerIDs:
			self.clientMsgs[p].append(msgEntry)

	# ----------------- Game Log Methods (All players) -----------------

	def stageLogEntry(self, msg: str):
		self.gameLog.addLogEntry(self.currentStateN, msg)

	def stageLogEntries(self, msgs: list):
		self.gameLog.addLogEntries(self.currentStateN, msgs)

	# ----------------- UI Methods -----------------	

	def stageUIChange(self, uiChange, playerID = None, playerIDs = None):
		"""playerID and playerIDs are optional, but don't pass more than one of them. If none are passed then it applies to all players."""
		self.stageUIChanges([uiChange], playerID=playerID, playerIDs=playerIDs)

	def stageUIChanges(self, uiChanges: list, playerID = None, playerIDs = None):
		"""playerID and playerIDs are optional, but don't pass more than one of them. If none are passed then it applies to all players."""
		if playerID:
			if playerIDs:
				raise ValueError("Received both arguments playerID and playerIDs")
			playerIDs = [playerID]
		elif not playerIDs:
			playerIDs = self.playerUIHistories.keys()
		assert(playerIDs)
		for uiChange in uiChanges:
			uiChange = deAliasUIChange(uiChange)
			for p in playerIDs:
				self.playerUIHistories[p].stageUIChange(uiChange)