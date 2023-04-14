import itertools
import flask

from pathlib import Path
from pathlib import PurePath

from .UIInterface import UIInterface
from .actions import ActionReceiver, decodeActionReceiver
from .UIHistory import UIHistory
from .GameLog import GameLog
from .UIState import encodeUIChange
from . import random



class GameManager(UIInterface, ActionReceiver):
	
	def __init__(self):
		random.seed()
		self.actionHistory = [] # A list of tuples (playerId, actionObj)
		self.playerUIHistories = {} # map from playerId to UIHistory object
		self.currentRevertN = 0
		self.currentStateN = 0
		self.gameLog = GameLog() # game log entries shared by players
		self.clientMsgs = {} # instant messages waiting to be sent to players
		self.arMap = {} # stores actionReciever objects by id

	# ----------------- Help Methods -----------------

	def _clampNumber(n, smallest, largest):
		return max(smallest, min(n, largest))
	
	def _popClientMessages(self, playerId):
		msgEntries = self.clientMsgs.get(playerId, [])
		if msgEntries:
			self.clientMsgs[playerId] = []
		return [("msg",) + m for m in msgEntries]

	def _getLogEntries(self, fromStateN, toStateN):
		logEntries = self.gameLog.getLogEntries(fromStateN, toStateN)
		return [("game_log",) + l for l in logEntries]

	def _getUIChanges(self, playerId, fromStateN, toStateN):
		if self.gameStarted():
			if playerId in self.playerUIHistories:
				assert(self.playerUIHistories[playerId].getCurrentStateN() == self.currentStateN)
				return self.playerUIHistories[playerId].getUIChanges(fromStateN, toStateN)
			else:
				print("Call to getUIChanges with invalid playerId: {}, fromStateN={}, toStateN={}.format(playerId, fromStateN, toStateN")
		else:
			return []

	def _advanceGameState(self, actionObj, playerId=None):
		# advance game state
		self.actionHistory.append((playerId, actionObj))
		self.currentStateN += 1
		for uiHistory in self.playerUIHistories.values():
			uiHistory.commitUIChanges()

	# ----------------- Server Methods -----------------
	
	def getGame(self):
		return self.game

	def setGame(self, game):
		""" should only be called once """
		assert(not hasattr(self, 'game'))
		self.game = game

	def getClientUpdates(self, playerId, revertN, fromStateN, toStateN):
		fromStateN = GameManager._clampNumber(fromStateN, 0, self.currentStateN)
		toStateN = GameManager._clampNumber(toStateN, 0, self.currentStateN)
		data = []
		if revertN != self.currentRevertN:
			# we reset the client and let it recreate divs and log from stateN zero
			data += [("reset_ui",), ("revert_n", self.currentRevertN)]
			fromStateN = 0
		data += [("state_n", toStateN)]
		data += self._popClientMessages(playerId)
		if self.gameStarted():
			data += self._getLogEntries(fromStateN, toStateN)
			data += self._getUIChanges(playerId, fromStateN, toStateN)
		return data
	
	def clientAction(self, currentRevertN, stateN, actionObj, playerId = None):
		if stateN != self.currentStateN:
			return False # TODO: respond 409 conflict?

		actionReceiver = decodeActionReceiver(self.arMap, actionObj["receiver"])
		actionArgs = tuple(actionObj.get("args", []))
		actionKwargs = actionObj.get("kwargs", {})
		assert(actionKwargs.get("playerId", None) == playerId)
		assert(isinstance(actionReceiver, ActionReceiver))
		assert(isinstance(actionArgs, tuple))
		assert(isinstance(actionKwargs, dict))
		if (actionReceiver is not self) and (not self.game.actionCheck(*actionArgs, **actionKwargs)):
			return False
		if actionReceiver.tryAction(*actionArgs, **actionKwargs):
			self._advanceGameState(actionObj, playerId)
			return True
		else:
			return False
			
	def startGame(self, playerIDs: list, playerNames: list):
		assert(not self.gameStarted())
		assert(self.currentRevertN == 0)
		for p in playerIDs:
			self.playerUIHistories[p] = UIHistory()
			self.clientMsgs[p] = []
		actionObj = {"receiver":self, "args":("start_game", playerIDs, playerNames)}
		res = self.clientAction(0, 0, actionObj)
		if res:
			print("Game started, playerIDs:", playerIDs)
		else:
			print("Error: Not allowed to start game, playerIDs:", playerIDs)
		return res

	def gameStarted(self):
		return self.currentStateN > 0

	def gameStartingUp(self):
		return self.playerUIHistories and not self.gameStarted()

	def revertToStateN(self, stateN):
		if stateN <= 0:
			random.seed()
		toStateN = GameManager._clampNumber(stateN, 1, self.currentStateN)
		if toStateN < self.currentStateN:
			assert(toStateN >= 1)
			# revert game state
			# go back to game state zero, and rebuild everything from there
			random.reset()
			fromStateN = self.currentStateN
			self.gameLog.clearLogEntries(0)
			actionsToReplay = self.actionHistory[0:toStateN]
			self.actionHistory = []
			self.game.resetGameState()
			self.currentRevertN += 1
			self.currentStateN = 0
			for uiHistory in self.playerUIHistories.values():
				uiHistory.revertTo(0)
			for playerId,actionObj in actionsToReplay:
				self.clientAction(self.currentRevertN, self.currentStateN, actionObj, playerId = playerId)
			if stateN <= 0:
				msg = "Current game was cleared. A new game has been setup.".format(fromStateN, toStateN)
			else:
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
	
	# --------------- "ActionReceiver" expected methods ---------------
	
	def tryAction(self, *args, playerId=None):
		if args[0] == "start_game":
			if self.gameStarted():
				# game has already been started
				raise RuntimeError("Tried to start game but game was already started.")
			self.game.startGame(args[1], args[2]) # pass playerIDs and playerNames
			return True
		return False

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

	def registerActionReceiver(self, actionReceiver, actionReceiverID):
		if not isinstance(actionReceiver, ActionReceiver):
			raise ValueError("actionReceiver must be of type ActionReceiver, not " + str(type(actionReceiver)))
		if not isinstance(actionReceiverID, str):
			raise ValueError("actionReceiverID must be of type string, not " + str(type(actionReceiverID)))
		self.arMap[actionReceiverID] = actionReceiver

	def stageUIChange(self, uiChange, playerID = None, playerIDs = None):
		"""playerID and playerIDs are optional, but don't pass more than one of them. If none are passed then it applies to all players."""
		self.stageUIChanges([uiChange], playerID=playerID, playerIDs=playerIDs)

	def stageUIChanges(self, uiChanges: list, playerID = None, playerIDs = None):
		"""playerID and playerIDs are optional, but don't pass more than one of them. If none are passed then it applies to all players."""
		if not (self.gameStarted() or self.gameStartingUp()):
			raise RuntimeError("Called stageUIChange/stageUIChanges at an incorrect state, game must be started or starting up!")
		if playerID:
			if playerIDs:
				raise ValueError("Received both arguments playerID and playerIDs")
			playerIDs = [playerID]
		elif not playerIDs:
			playerIDs = self.playerUIHistories.keys()
		assert(playerIDs)
		for uiChange in uiChanges:
			uiChange,isOriginal = encodeUIChange(self.arMap, uiChange, False)
			for p in playerIDs:
				self.playerUIHistories[p].stageUIChange(uiChange)