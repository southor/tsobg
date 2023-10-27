import sys
from pathlib import Path
import random
from copy import deepcopy

pathHere = Path(__file__).absolute().parent

# import tsobg GameInterface
sys.path.append(str(pathHere.parent.parent))
print(pathHere.parent.parent)
from tsobg import GameInterface, ActionReceiver

# import SkyScrapers cards
#sys.path.append(str(pathHere.parent))
#import card_graphics
from Card import checkCardImageFiles
from PlayerArea import PlayerArea
from CardMarket import CardMarket
from MainBoard import MainBoard


class SkyscrapersGame(GameInterface, ActionReceiver):

	playerStartSupply = {"money":12}

	gameStateVars = ["playerIDs", "playersSupply", "playerAreas", "cardMarket", "mainBoard", "gamePhase", "currentPlayer"]

	def __init__(self, gameManager):
		self.gameManager = gameManager
		msg = checkCardImageFiles()
		if msg:
			print(msg)
		
	# --------------- Game methods ---------------
	
	def addTestImage(self):
		"""
		uic = ("set_div", {"id":"deck_outline1",
							"parent":"center",
							"pos":[70, 65],
							"size": card_graphics.cardSize,
							"color": "white",
							"border": "solid #A0A0A0"})
		self.addUIChange(uic)
		
		uic = ("set_div", {"id":"deck_outline2",
							"parent":"deck_outline1",
							"pos":[10, -10],
							"size": card_graphics.cardSize,
							"color": "white",
							"border": "solid #A0A0A0"})
		self.addUIChange(uic)
		
		uic = ("set_div", {"id":"deck_outline3",
							"parent":"deck_outline2",
							"pos":[10, -10],
							"size": card_graphics.cardSize,
							"color": "white",
							"border": "solid #A0A0A0"})
		self.addUIChange(uic)
		"""
		# test add image
		#print(self.getURLFor("architect01.png"))
		uic = ("set_div", "test_card", {
							"parent":"center",
							"pos":[70, 65],
							#"size": card_graphics.cardSize,
							#"img":"game_file/generated_cards/architect01.png",
							"img":"game_file/generated_cards_online/card_architect03.png",
							#"border": "solid #A0A0A0"
							})
		self.stageUIChange(uic)

	def getCurrentPlayerID(self) -> str:
		if not hasattr(self, 'playerIDs'):
			return None
		return self.playerIDs[self.currentPlayer]

	def getCurrentPlayerName(self) -> str:
		if not self.playerNames:
			return None
		return self.playerNames[self.currentPlayer]

	def getCurrentPlayerArea(self) -> PlayerArea:
		if not self.playerAreas:
			return None
		return self.playerAreas[self.currentPlayer]

	def nextPlayer(self):
		self.currentPlayer = (self.currentPlayer + 1) % len(self.playerIDs)
	
	# --------------- "GameInterface" expected methods ---------------

	def getName(self):
		return "Skyscrapers"

	def getRootPath(self):
		return pathHere.parent

	def resetGameState(self):
		""" reset game state to the same as after __init__"""
		selfVars = vars(self)
		for k in self.gameStateVars:
			if k in selfVars:
				selfVars.pop(k)

	def startGame(self, playerIDs: list, playerNames: list):
		gameIsStarted = hasattr(self, "playerIDs")
		assert(not gameIsStarted)
		# check card image files
		text = checkCardImageFiles()
		if text:
			self.gameManager.sendMessageToPlayers(("error", text))
		# init game
		self.gameManager.registerActionReceiver(self, self.getName())
		self.playerIDs = playerIDs
		self.playerNames = playerNames
		self.gamePhase = "cards_phase"
		self.currentPlayer = 0
		self.gameManager.stageUIChange(("set_div", "game_area", {"width":1015}))
		self.gameManager.stageUIChange(("set_div", "center", {"parent": "game_area", "class": "game-surface", "width":1000}))
		self.cardMarket = CardMarket(self.gameManager)
		self.mainBoard = MainBoard(self.gameManager)
		self._initPlayerSurfaces(playerNames)
		self._initPlayerAreas()
		self.cardMarket.fillUp()
		self.mainBoard.setFloors(3,1, ["shop", "office", "office"])
		self.gameManager.stageLogEntry("Game started, players: " + ", ".join(playerNames))

	def actionCheck(self, *args, playerId=None, **kwargs):
		if playerId != self.getCurrentPlayerID():
			if playerId == None:
				raise RuntimeError("recieved kwargs without playerId")
			else:
				#return "It is not your turn!"
				self.gameManager.sendMessageToPlayer(("info", "It is not your turn!"), playerId)
				return False
		return True
	
	# --------------- "ActionReceiver" expected methods ---------------

	def tryAction(self, *args, playerId=None, **kwargs):
		gameHasStarted = hasattr(self, "playerIDs")
		action = args[0]
		if action not in ["take_card"]:
			self.gameManager.sendMessageToPlayer(("error", "Unknown action: " + str(args)), playerId)
			return False
		if not gameHasStarted:
			# game has not been started yet
			if playerId == None:
				raise RuntimeError("Received invalid action args (game not started yet): " + str(args))
			else:
				self.gameManager.sendMessageToPlayer(("error", "Cannot perform action {}, game has not started yet!".format(action)), playerId)
				return False
		if self.gamePhase == "cards_phase" and action == "take_card":
			return self._actionTakeCard(args[1])
		else:
			self.gameManager.sendMessageToPlayer(("info", "Action {} not allowed in the {} phase.".format(action, self.gamePhase)), playerId)
			

	# --------------- Setup / Action Methods ---------------

	def _getPlayerSurfaceDivID(seatN):
		return "player_surface_" + str(seatN)

	def _initPlayerSurfaces(self, playerNames: list):
		nPlayers = len(self.playerIDs)
		# create divs but add to parent in viewed order (unique for each player)
		divOpts = {"parent":"game_area", "class":"game-surface", "size":(1000, 280)}
		for viewingSeatN,playerID in enumerate(self.playerIDs):
			appearedOrder_divIds = [0] * nPlayers
			for i in range(viewingSeatN, viewingSeatN + nPlayers):
				viewedSeatN = i % nPlayers
				appearedSeatN = i - viewingSeatN
				divID = SkyscrapersGame._getPlayerSurfaceDivID(viewedSeatN)
				self.gameManager.stageUIChange(("set_div", divID, {"text":playerNames[viewedSeatN]}))
				appearedOrder_divIds[appearedSeatN] = divID # save divId in appeared order for later
			# set div parent and rest of divopts in appearedOrder (for this player)
			for divID in appearedOrder_divIds:
				self.gameManager.stageUIChange(("set_div", divID, divOpts), playerID=playerID)

	def _initPlayerAreas(self):		
		self.playersSupply = [SkyscrapersGame.playerStartSupply.copy() for p in self.playerIDs]
		self.playerAreas = []
		for seatN,items in enumerate(self.playersSupply):
			playerSurfaceDivID = SkyscrapersGame._getPlayerSurfaceDivID(seatN)
			self.playerAreas.append(PlayerArea(self.gameManager, self, seatN, playerSurfaceDivID, items))

	def _actionTakeCard(self, cardId):
		playerArea = self.getCurrentPlayerArea()
		if playerArea.nFreeSpaces() == 0:
			self.gameManager.sendMessageToPlayer(("info", "Cannot take card, player area is full!"), self.getCurrentPlayerID())
			return False
		card = self.cardMarket.removeCard(cardId)
		if card:
			playerArea.addCard(card)
			self.gameManager.stageLogEntry(self.getCurrentPlayerName() + " took " + cardId)
			self.nextPlayer()
			return True
		else:
			self.gameManager.sendMessageToPlayer(("error", "card " + cardId + " could not be taken, does not exist in the market!"), self.getCurrentPlayerID())
			return False
		
		
		
		