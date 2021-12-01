import sys
from pathlib import Path

pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent.parent))
import tsobg

from SkyscrapersGame import SkyscrapersGame

# for testing
nPlayers = 1
players = {'Bosse':'10f8cf24'}


if __name__ == '__main__':
	
	if 'nPlayers' in globals():
		nPlayers = globals()['nPlayers']
	else:
		nPlayers = input("Input number of players: ")
	
	kwargs = {}
	if 'players' in globals():
			kwargs['players'] = globals()['players']
	
	tsobg.newGame(SkyscrapersGame(), int(nPlayers), **kwargs)
	tsobg.runServer(True)
	
	