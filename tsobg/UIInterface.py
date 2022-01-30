

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

	def stageUIChange(self, uiChange, playerID = None, playerIDs = None):
		"""playerID and playerIDs are optional, but don't pass more than one of them. If none are passed then it applies to all players."""
		pass

	def stageUIChanges(self, uiChanges: list, playerID = None, playerIDs = None):
		"""playerID and playerIDs are optional, but don't pass more than one of them. If none are passed then it applies to all players."""
		pass