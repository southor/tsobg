

class UIInterface:

	# ----------------- Client Message methods -----------------
	
	def sendMessageToPlayer(self, msgEntry, playerID):
		""" Arg msgEntry (tuple): (type, text) """
		pass

	def sendMessageToPlayers(self, msgEntry, playerIDs = None):
		""" 
		Args:
			msgEntry (tuple): (type, text)
			playerIDs (iterable): optional, if not provided message goes to all players
		"""
		pass
	
	# ----------------- Game Log Methods -----------------
	
	def stageLogEntry(self, msg):
		pass

	def stageLogEntries(self, msgs):
		pass

	# ----------------- UI Methods -----------------

	def stageUIChange_OnePlayer(self, playerID, uiChange):
		pass
	
	def stageUIChange_SomePlayers(self, playerIDs, uiChange):
		pass

	def stageUIChange_AllPlayers(self, uiChange):
		pass

	def stageUIChanges_OnePlayer(self, playerIDs, uiChanges: list):
		pass
	
	def stageUIChanges_SomePlayers(self, playerIDs, uiChanges: list):
		pass
		
	def stageUIChanges_AllPlayers(self, uiChanges: list):
		pass