import secrets, logging, flask
from flask import Flask, render_template, jsonify, send_file, Response
app = Flask(__name__)

werkzeugLogger = logging.getLogger('werkzeug')
werkzeugLogger.setLevel(logging.ERROR)

from pathlib import PurePath

app.config['SECRET_KEY'] = '121504121e437d2905d3fe067bfa8e29'

admin_key = '905d3fe067bf'
# http://127.0.0.1:5000/get_state/905d3fe067bf
# http://127.0.0.1:5000/modify_turn/905d3fe067bf/1/0

#state_test = [1, 2, 0]

#user_states = {}

game = None
players = {} # playerName to playerIDs dict
nPlayers = 0

def _getPlayerNames():
	return list(globals()['players'].keys())

def _createPlayer(playerName):
	global players
	global game
	if enoughPlayers():
		print("Player count already filled up!")
		return None
	elif playerName in players:
		print("player already exists:", playerName)
		return None
	else:
		playerId = secrets.token_hex(4)
		players[playerName] = playerId
		print("created player:", playerId, playerName)
		if enoughPlayers():
			game.startGame(list(players.values()), list(players.keys())) # relying on order being the same for keys() and values()
		return playerId

def enoughPlayers():
	global players
	global nPlayers
	return len(players) >= nPlayers


@app.route("/", methods=['GET'])
def startPage():
	if enoughPlayers():
		return renderError("Player count already filled up!")
	else:
		return render_template('start.html', gameName=game.name, nPlayers=nPlayers, done=False)

@app.route("/new_player/<playerName>", methods=['GET', 'POST'])
def createPlayer(playerName):
	res = _createPlayer(playerName)
	if res:
		return jsonify(res)
	else:
		flask.abort(405)

def checkPlayerID(playerId, playerName):
	global players
	if (playerName not in players):
		return "player does not exist: " + playerName
	if (playerId != players[playerName]):
		return "playerName - playerId mismatch: " + playerName + " " + playerId
	else:
		return None
		
def renderError(msg):
	print("Error:", msg)
	return render_template('error.html', gameName=game.name, msg=msg)

@app.route("/game/<playerId>/<playerName>/view", methods=['GET'])
def gamePage(playerId, playerName):
	global game
	global players
	global nPlayers
	msg = checkPlayerID(playerId, playerName)
	if msg:
		return renderError(msg)
	else:
		pageTitle = game.name + " ({} players)".format(str(nPlayers))
		info = "" if enoughPlayers() else "waiting for other players..."
		return render_template('game.html', pageTitle=pageTitle, playerId=playerId, playerName=playerName, info=info)

@app.route("/game/<playerId>/<playerName>/update_client/<fromStateN>", methods=['GET'])
def updateClient(playerId, playerName, fromStateN):
	global game
	return updateClientTo(playerId, playerName, int(fromStateN), game.currentStateN)

@app.route("/game/<playerId>/<playerName>/update_client/<fromStateN>/<toStateN>", methods=['GET'])
def updateClientTo(playerId, playerName, fromStateN, toStateN):
	global game
	if checkPlayerID(playerId, playerName) != None:
		flask.abort(409)
	fromStateN = int(fromStateN)
	toStateN = int(toStateN)
	#print("updateClientTo: ", playerId, playerName, fromStateN, toStateN)
	data = game.getClientUpdates(playerId, fromStateN, toStateN)
	return jsonify(data)

@app.route("/game/<playerId>/<playerName>/client_action/<stateN>", methods=['POST'])
def clientAction(playerId, playerName, stateN):
	global game
	if checkPlayerID(playerId, playerName) != None:
		flask.abort(409)
	if not flask.request.is_json:
		print("not json, instead: ", flask.request.content_type)
		flask.abort(400)
	actionObj = flask.request.get_json()
	print("client action:", actionObj)
	if game.clientAction(int(stateN), actionObj):
		return updateClient(playerId, playerName, stateN)
	else:
		return Response("action not allowed", status=403, mimetype='application/json')

@app.route("/game/<playerId>/<playerName>/game_file/<path:gameFilePath>", methods=['GET'])
def gameFile(playerId, playerName, gameFilePath):
	global game
	if checkPlayerID(playerId, playerName) != None:
		flask.abort(409)
	gameFilePath = PurePath(gameFilePath)
	print("wants to get file:", gameFilePath)
	if "." in str(gameFilePath.parent):
		flask.abort(403)
	filePath = game.getFullPath(gameFilePath)
	if filePath:
		if filePath.is_file():
			print("sending file: ", filePath)
			return send_file(str(filePath))
		else:
			flask.abort(404)
	else:
		flask.abort(403)

def newGame(game, nPlayers, **kwargs):
	assert(not game.hasStarted())
	globals()['game'] = game
	globals()['nPlayers'] = nPlayers
	if 'players' in kwargs:
		players = kwargs['players']
		assert(isinstance(players, dict))
		assert(len(players) <= nPlayers)
		globals()['players'] = players
	else:
		players = globals()['players']
	if enoughPlayers():
		game.startGame(list(players.values()), list(players.keys())) # relying on order being the same for keys() and values()

def runServer(debug):
	global players
	for seatN,playerName in enumerate(players.keys()):
		print("url for player " + str(seatN) + ": http://127.0.0.1:5000/" + "game/" + players[playerName] + "/" + playerName + "/view")
	app.run(debug=debug, threaded=False, processes=1)

if __name__ == '__main__':
	#app.run(debug=True)
	runServer(True)