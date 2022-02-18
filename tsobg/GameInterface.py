
class GameInterface:
	
	def getName(self):
		pass

	def getRootPath(self):
		pass

	def actionAllowed(self, actionObj, playerId=None):
		pass
	
	def performAction(self, actionObj, playerId=None):
		pass
	
	def resetGameState(self):
		""" reset game state to the same as after __init__"""
		pass


