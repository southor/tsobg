from .actions import ActionReceiver

class GameInterface():
	
	def getName(self):
		pass

	def getRootPath(self):
		pass

	def actionCheck(self, actionArgs, playerId):
		""" 
		Used to check if an action is valid before tryAAction is called.
		If it returns True then tryAction is called for the ActionReceiver, if it returns False then tryAction is skipped.
		"""
		pass

	def resetGameState(self):
		""" reset game state to the same as after __init__"""
		pass

	def startGame(self, playerIDs: list, playerNames: list):
		""" Is called when game should start and provides the player ids and names """
		pass

