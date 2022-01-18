import sys
from pathlib import Path
import random

pathHere = Path(__file__).absolute().parent

# import tsobg BaseGame
sys.path.append(str(pathHere.parent.parent))
from tsobg import BaseGame

# import SkyScrapers cards
#sys.path.append(str(pathHere.parent))
#import card_graphics
from Card import checkCardImageFiles
from PlayerArea import PlayerArea
from CardMarket import CardMarket


class SkyscrapersGame(BaseGame):

	playerStartSupply = {"money":12}

	gameStateVars = ["playerIDs", "playersSupply", "currentPlayer", "playerAreas", "cardMarket"]

	def __init__(self):
		gameRootPath = pathHere.parent
		super().__init__("Skyscrapers", gameRootPath)
		msg = checkCardImageFiles()
		if msg:
			print(msg)
		self.cardMarket = CardMarket(self)
		
	# --------------- Helper methods ---------------
		
	# exports game state as a dictionary
	def __exportGameState(self):
		# TODO: implement compression (card/cardId can be just an int)
		selfVars = vars(self)
		return {v: selfVars[v] for v in self.gameStateVars}
		
	# TODO: create class for UIChange ?
		
	# TODO: create class for actionObj ?
	
	def __importGameState(self):
		# TODO
		raise RuntimeException("Not implemented")
	
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
	
	# --------------- "BaseGame" expected methods ---------------

	def getInfoTexts(self):
		msg = checkCardImageFiles()
		return [msg] if msg else []
	
	def actionAllowed(self, actionObj):
		if actionObj[0] == "start_game":
			return False if hasattr(self, "players") else True
		elif actionObj[0] == "take_card":
			return True
		else:
			print("Error, unknown action", actionObj)
			return False
	
	def performAction(self, actionObj):
		assert(self.actionAllowed(actionObj))
		if actionObj[0] == "start_game":
			self.__actionStartGame(actionObj[1], actionObj[2]) # pass playerIDs and playerNames
		elif actionObj[0] == "take_card":
			self.cardMarket.removeCard(actionObj[1])
		else:
			print("Error, unknown action", actionObj)
		return self.__exportGameState()
		
	# --------------- Action Methods ---------------

	def __getPlayerSurfaceDivID(seatN):
		return "player_space_" + str(seatN)

	def __initPlayerSurfaces(self, playerNames: list):
		nPlayers = len(self.playerIDs)
		divOpts = {"parent":"game_area", "class":"player-surface",  "size":(800, 280)}
		# set basic div opts
		for seatN,playerName in enumerate(playerNames):
			divID = SkyscrapersGame.__getPlayerSurfaceDivID(seatN)
			self.stageUIChange_AllPlayers(("set_div", divID, divOpts))
			self.stageUIChange_AllPlayers(("set_div", divID, {"text":playerName}))
		# set div pos (unique for each player)
		offset = 520
		for viewingSeatN,playerID in enumerate(self.playerIDs):
			for i in range(viewingSeatN, viewingSeatN + nPlayers):
				viewedSeatN = i % nPlayers
				appearedSeatN = i - viewingSeatN
				divID = SkyscrapersGame.__getPlayerSurfaceDivID(viewedSeatN)
				divOpts = { "pos": (0, offset + appearedSeatN * 300) }
				self.stageUIChange_OnePlayer(playerID, ("set_div", divID, divOpts))
	
	def __initPlayerAreas(self):		
		self.playersSupply = [SkyscrapersGame.playerStartSupply.copy() for p in self.playerIDs]
		self.playerAreas = []
		for seatN,items in enumerate(self.playersSupply):
			playerSurfaceDivID = SkyscrapersGame.__getPlayerSurfaceDivID(seatN)
			self.playerAreas.append(PlayerArea(self, seatN, playerSurfaceDivID, items))

	def __actionStartGame(self, playerIDs: list, playerNames: list):
		self.playerIDs = playerIDs
		self.currentPlayer = 0
		self.__initPlayerSurfaces(playerNames)
		self.__initPlayerAreas()
		self.cardMarket.fillUp()
		self.stageUIChange_AllPlayers(("set_div", "center", {"size": (800, 500)}))
		
		
		
		