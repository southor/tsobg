import sys
from pathlib import Path
import random
from copy import deepcopy

pathHere = Path(__file__).absolute().parent

# import tsobg GameInterface
sys.path.append(str(pathHere.parent.parent))
from tsobg import GameInterface

# import SkyScrapers cards
#sys.path.append(str(pathHere.parent))
#import card_graphics
from Card import checkCardImageFiles
from PlayerArea import PlayerArea
from CardMarket import CardMarket
from MainBoard import MainBoard


class SkyscrapersGame(GameInterface):

	playerStartSupply = {"money":12}

	gameStateVars = ["playerIDs", "playersSupply", "playerAreas", "cardMarket", "mainBoard", "gamePhase", "currentPlayer"]

	def __init__(self, gameManager):
		self.gameManager = gameManager
		#gameRootPath = pathHere.parent
		#super().__init__("Skyscrapers", gameRootPath)
		msg = checkCardImageFiles()
		if msg:
			print(msg)
		
	# --------------- Helper methods ---------------
	
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
	
	# --------------- "GameInterface" expected methods ---------------

	def getName(self):
		return "Skyscrapers"

	def getRootPath(self):
		return pathHere.parent

	def getCurrentPlayerID(self):
		if not self.playerIDs:
			return None
		return self.playerIDs[self.currentPlayer]

	def getCurrentPlayerName(self):
		if not self.playerNames:
			return None
		return self.playerNames[self.currentPlayer]

	def nextPlayer(self):
		self.currentPlayer = (self.currentPlayer + 1) % len(self.playerIDs)
	
	"""
	def actionAllowed(self, actionObj, playerId=None):
		if actionObj[0] == "start_game":
			return not hasattr(self, "playerIDs")
		elif actionObj[0] == "take_card":
			return True
		else:
			print("Error, unknown action", actionObj)
			return False
	"""
	
	def tryAction(self, actionObj, playerId=None):
		#
		#""" Returns None if action succedded, returns a string with message if action failed """
		#assert(self.actionAllowed(actionObj))
		action = actionObj[0]
		if action == "start_game":
			if hasattr(self, "playerIDs"):
				# game has already been started?
				raise RuntimeError("Tried to start game but playerIDs is already set in SkyscrapersGame object")
			self.__actionStartGame(actionObj[1], actionObj[2]) # pass playerIDs and playerNames
			return True
		if playerId != self.getCurrentPlayerID():
			if playerId == None:
				raise RuntimeError("recieved actionObj without playerId: ", actionObj)
			else:
				#return "It is not your turn!"
				self.gameManager.sendMessageToPlayer(("info", "It is not your turn!"), playerId)
				return False
		if action not in ["take_card"]:
			self.gameManager.sendMessageToPlayer(("error", "Unknown action: " + str(actionObj)), playerId)
			return False
		if self.gamePhase == "cards_phase" and action == "take_card":
			if self.cardMarket.removeCard(actionObj[1]):
				self.gameManager.stageLogEntry(self.getCurrentPlayerName() + " took " + actionObj[1])
				self.nextPlayer()
				return True
			else:
				self.gameManager.sendMessageToPlayer(("error", "card " + actionObj[1] + " could not be taken, does not exists in the market!"), playerId)
				return False
		else:
			self.gameManager.sendMessageToPlayer(("info", "Action {} not allowed in the {} phase.".format(action, self.gamePhase)), playerId)
			

	def resetGameState(self):
		""" reset game state to the same as after __init__"""
		selfVars = vars(self)
		for k in self.gameStateVars:
			if k in selfVars:
				selfVars.pop(k)
		
	# --------------- Action Methods ---------------

	def __getPlayerSurfaceDivID(seatN):
		return "player_space_" + str(seatN)

	def __initPlayerSurfaces(self, playerNames: list):
		nPlayers = len(self.playerIDs)
		# create divs but add to parent in viewed order (unique for each player)
		divOpts = {"parent":"game_area", "class":"game-surface", "size":(1000, 280)}
		for viewingSeatN,playerID in enumerate(self.playerIDs):
			appearedOrder_divIds = [0] * nPlayers
			for i in range(viewingSeatN, viewingSeatN + nPlayers):
				viewedSeatN = i % nPlayers
				appearedSeatN = i - viewingSeatN
				divID = SkyscrapersGame.__getPlayerSurfaceDivID(viewedSeatN)
				self.gameManager.stageUIChange(("set_div", divID, {"text":playerNames[viewedSeatN]}))
				appearedOrder_divIds[appearedSeatN] = divID # save divId in appeared order for later
			# set div parent and rest of divopts in appearedOrder (for this player)
			for divID in appearedOrder_divIds:
				self.gameManager.stageUIChange(("set_div", divID, divOpts), playerID=playerID)

	def __initPlayerAreas(self):		
		self.playersSupply = [SkyscrapersGame.playerStartSupply.copy() for p in self.playerIDs]
		self.playerAreas = []
		for seatN,items in enumerate(self.playersSupply):
			playerSurfaceDivID = SkyscrapersGame.__getPlayerSurfaceDivID(seatN)
			self.playerAreas.append(PlayerArea(self.gameManager, seatN, playerSurfaceDivID, items))

	def __actionStartGame(self, playerIDs: list, playerNames: list):
		# check card image files
		text = checkCardImageFiles()
		if text:
			self.gameManager.sendMessageToPlayers(("error", text))
		# init game
		self.playerIDs = playerIDs
		self.playerNames = playerNames
		self.gamePhase = "cards_phase"
		self.currentPlayer = 0
		self.gameManager.stageUIChange(("set_div", "center", {"parent": "game_area", "class": "game-surface", "width":1000}))
		self.cardMarket = CardMarket(self.gameManager)
		self.mainBoard = MainBoard(self.gameManager)
		self.__initPlayerSurfaces(playerNames)
		self.__initPlayerAreas()
		self.cardMarket.fillUp()
		self.mainBoard.setFloors(3,1, ["shop", "office", "office"])
		self.gameManager.stageLogEntry("Game started, players: " + ", ".join(playerNames))
		
		
		
		