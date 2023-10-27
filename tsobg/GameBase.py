from .GameInterface import GameInterface


class GameBase(GameInterface):
	
	_gameStateVars = ["playerIDs", "currentPlayer"]

	def __init__(self, gameManager):
		self.gameManager = gameManager

	def getCurrentPlayerID(self) -> str:
		if not hasattr(self, 'playerIDs'):
			return None
		return self.playerIDs[self.currentPlayer]

	def getCurrentPlayerName(self) -> str:
		if not self.playerNames:
			return None
		return self.playerNames[self.currentPlayer]

	# --------------- "GameInterface" expected methods ---------------

	def resetGameState(self):
		""" reset game state to the same as after __init__"""
		selfVars = vars(self)
		for k in self._gameStateVars:
			if k in selfVars:
				selfVars.pop(k)

	def startGame(self, playerIDs: list, playerNames: list):
		gameIsStarted = hasattr(self, "playerIDs")
		assert(not gameIsStarted)
		# init game
		self.playerIDs = playerIDs
		self.playerNames = playerNames
		self.currentPlayer = 0
		self.gameManager.stageUIChange(("set_div", "game_area", {"width":1015}))
		self.gameManager.stageUIChange(("set_div", "center", {"parent": "game_area", "class": "game-surface", "width":1000}))

	# --------------- Setup Methods ---------------

	def getPlayerSurfaceDivID(seatN):
		return "player_surface_" + str(seatN)

	def initPlayerSurfaces(self) -> list:
		nPlayers = len(self.playerIDs)
		# create divs but add to parent in viewed order (unique for each player)
		divOpts = {"parent":"game_area", "class":"game-surface", "size":(1000, 280)}
		for viewingSeatN,playerID in enumerate(self.playerIDs):
			appearedOrder_divIds = [0] * nPlayers
			for i in range(viewingSeatN, viewingSeatN + nPlayers):
				viewedSeatN = i % nPlayers
				appearedSeatN = i - viewingSeatN
				divID = GameBase.getPlayerSurfaceDivID(viewedSeatN)
				self.gameManager.stageUIChange(("set_div", divID, {"text":self.playerNames[viewedSeatN]}))
				appearedOrder_divIds[appearedSeatN] = divID # save divId in appeared order for later
			# set div parent and rest of divopts in appearedOrder (for this player)
			for divID in appearedOrder_divIds:
				self.gameManager.stageUIChange(("set_div", divID, divOpts), playerID=playerID)
		return [GameBase.getPlayerSurfaceDivID(seatN) for seatN in range(nPlayers)]

	def addGameStateVar(self, name):
		self._gameStateVars.append(name)

	def addGameStateVars(self, names: list):
		self._gameStateVars += names
