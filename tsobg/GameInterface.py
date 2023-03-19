from .ActionReceiver import ActionReceiver

class GameInterface(ActionReceiver):
	
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

	def tryAction(self, actionArgs):
		""" 
		Used only for startGame action, other actions are called on the actionReceiver for each action.
		"""
		pass

	def resetGameState(self):
		""" reset game state to the same as after __init__"""
		pass


