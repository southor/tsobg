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
from CardMarket import CardMarket


class SkyscrapersGame(BaseGame):

	playerStartSupply = {"money":12}

	gameStateVars = ["players", "playerSupply", "currentPlayer", "cardMarket"]

	def __init__(self):
		gameRootPath = pathHere.parent
		super().__init__("Skyscrapers", gameRootPath)
		self.cardMarket = CardMarket(self)
		
	# --------------- Helper methods ---------------
		
	# exports game state as a dictionary
	def __exportGameState(self):
		selfVars = vars(self)
		return {v: selfVars[v] for v in self.gameStateVars}
		
	# TODO: create class for UIChange ?
		
	# TODO: create class for actionObj ?
	
	# TODO: If needed BaseGame can later ask SkyscrapersGame to load a "GameState", by passing an old dictionary.
	#       GameState dictionaries can be stored to disk.
	
	def addTestImage(self):
		"""
		uic = ["set_div", {"id":"deck_outline1",
							"parent":"center",
							"pos":[70, 65],
							"size": card_graphics.cardSize,
							"color": "white",
							"border": "solid #A0A0A0"}]
		self.addUIChange(uic)
		
		uic = ["set_div", {"id":"deck_outline2",
							"parent":"deck_outline1",
							"pos":[10, -10],
							"size": card_graphics.cardSize,
							"color": "white",
							"border": "solid #A0A0A0"}]
		self.addUIChange(uic)
		
		uic = ["set_div", {"id":"deck_outline3",
							"parent":"deck_outline2",
							"pos":[10, -10],
							"size": card_graphics.cardSize,
							"color": "white",
							"border": "solid #A0A0A0"}]
		self.addUIChange(uic)
		"""
		# test add image
		#print(self.getURLFor("architect01.png"))
		uic = ["set_div", {"id":"test_card",
							"parent":"center",
							"pos":[70, 65],
							#"size": card_graphics.cardSize,
							#"img":"game_file/generated_cards/architect01.png",
							"img":"game_file/generated_cards_online/architect01.png",
							#"border": "solid #A0A0A0"
							}]
		self.addUIChange(uic)
	
	# --------------- "BaseGame" expected methods ---------------
	
	def actionAllowed(self, actionObj):
		if actionObj[0] == "start_game":
			return False if hasattr(self, "players") else True
		else:
			# TODO: throw error?
			print("Error, unknown action", actionObj)
			return False
	
	def performAction(self, actionObj):
		assert(self.actionAllowed(actionObj))
		if actionObj[0] == "start_game":
			self.__actionStartGame(actionObj[1]) # pass players
		else:
			# TODO: throw error?
			print("Error, unknown action", actionObj)
		return self.__exportGameState()
		
	# --------------- Action Methods ---------------
	
	def __initPlayersSupply(self):
		self.playerSupply = [SkyscrapersGame.playerStartSupply.copy() for p in self.players]
	
	def __actionStartGame(self, players: list):
		self.players = players
		self.currentPlayer = 0
		self.__initPlayersSupply()
		self.cardMarket.fillUp()
		# TODO initiate rest of UI stuff here by calling BaseClass's self.addUIChange(uiChange)
		self.addTestImage()
		
		
		