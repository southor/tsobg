# See README.md

import sys
from pathlib import Path

pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent.parent))
import tsobg

from SkyscrapersGame import SkyscrapersGame

import game_settings


if __name__ == '__main__':
	
	try:
		nPlayers = game_settings.nPlayers
	except AttributeError:
		nPlayers = input("Input number of players: ")
	
	kwargs = {}
	try:
		kwargs['players'] = game_settings.players
	except AttributeError:
		pass # let kwargs be empty
	
	tsobg.newGame(SkyscrapersGame, int(nPlayers), **kwargs)
	tsobg.runServer(False)
	