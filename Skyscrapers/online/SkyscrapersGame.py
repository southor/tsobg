import sys
from pathlib import Path
import random

pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent.parent))
from tsobg import BaseGame

import game



class SkyscrapersGame(BaseGame):

	gameStateVars = ["players", "currentPlayer"] # TODO: add "deck"

	def __init__(self):
		gameRootPath = pathHere.parent
		super().__init__("Skyscrapers", gameRootPath)
		
	# --------------- Helper methods ---------------
		
	# exports game state as a dictionary
	def __exportGameState(self):
		selfVars = vars(self)
		return {v: selfVars[v] for v in self.gameStateVars}
		
	# TODO: create class for UIChange ?
		
	# TODO: create class for actionObj ?
	
	# TODO: If needed BaseGame can later ask SkyscrapersGame to load a "GameState", by passing an old dictionary.
	#       GameState dictionaries can be stored to disk.
	
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
	
	def __actionStartGame(self, players: list):
		self.players = players
		self.currentPlayer = 0
		
		# TODO initiate all UI stuff here by calling BaseClass's self.addUIChange(uiChange)
		
		# test add image
		#print(self.getURLFor("architect01.png"))
		uic = ["set_div", {"id":"test_card", "parent":"center", "pos":[100, 35], "img":"game_file/generated_cards/architect01.png"}]
		self.addUIChange(uic)
		