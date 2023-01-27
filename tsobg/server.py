import secrets
import logging
import flask
from flask import Flask, render_template, jsonify, send_file, Response
app = Flask(__name__)

werkzeugLogger = logging.getLogger('werkzeug')
werkzeugLogger.setLevel(logging.ERROR)

from pathlib import PurePath

from .debug import createDebugPageHTML
from .GameManager import GameManager
from . import settings


app.config['SECRET_KEY'] = '121504121e437d2905d3fe067bfa8e29'


# http://127.0.0.1:5000/get_state/905d3fe067bf
# http://127.0.0.1:5000/modify_turn/905d3fe067bf/1/0

#state_test = [1, 2, 0]

#user_states = {}

gameManager = None
players = {} # playerName to playerIDs dict
nPlayers = 0

def _getGameName():
	return gameManager.getGame().getName()

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
			gameManager.startGame(list(players.values()), list(players.keys())) # relying on order being the same for keys() and values()
		return playerId

def enoughPlayers():
	global players
	global nPlayers
	return len(players) >= nPlayers

@app.route("/", methods=['GET'])
def rootPage():
	return flask.redirect("/start")

@app.route("/start", methods=['GET'])
def startPage():
	if enoughPlayers():
		return renderMsgPage("Player count already filled up!")
	else:
		return render_template('start.html', gameName=_getGameName(), nPlayers=nPlayers, done=False)

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

def renderMsgPage(msg, link="", linkText=""):
	return render_template('msg.html', gameName=_getGameName(), msg=msg, link=link, linkText=linkText)

def renderErrorPage(msg, link="", linkText=""):
	print("Error:", msg)
	return render_template('error.html', gameName=_getGameName(), msg=msg, link=link, linkText=linkText)

@app.route("/game/<playerId>/<playerName>/view", methods=['GET'])
def gamePage(playerId, playerName):
	global game
	global players
	global nPlayers
	msg = checkPlayerID(playerId, playerName)
	if msg:
		return renderErrorPage(msg, "/start", "to start page")
	else:
		pageTitle = _getGameName() + " ({} players)".format(str(nPlayers))
		info = "" if enoughPlayers() else "waiting for other players..."
		return render_template('game.html', pageTitle=pageTitle, playerId=playerId, playerName=playerName, info=info)

@app.route("/game/<playerId>/<playerName>/update_client/<revertN>/<fromStateN>", methods=['GET'])
def updateClient(playerId, playerName, revertN, fromStateN):
	global game
	return updateClientTo(playerId, playerName, int(revertN), int(fromStateN), gameManager.currentStateN)

@app.route("/game/<playerId>/<playerName>/update_client/<revertN>/<fromStateN>/<toStateN>", methods=['GET'])
def updateClientTo(playerId, playerName, revertN, fromStateN, toStateN):
	global game
	if checkPlayerID(playerId, playerName) != None:
		flask.abort(409)
	data = gameManager.getClientUpdates(playerId, int(revertN), int(fromStateN), int(toStateN))
	return jsonify(data)

@app.route("/game/<playerId>/<playerName>/client_action/<revertN>/<stateN>", methods=['POST'])
def clientAction(playerId, playerName, revertN, stateN):
	global game
	if checkPlayerID(playerId, playerName) != None:
		flask.abort(409)
	if not flask.request.is_json:
		print("not json, instead: ", flask.request.content_type)
		flask.abort(400)
	actionObj = flask.request.get_json()
	print("client action:", actionObj)
	#if gameManager.clientAction(int(revertN), int(stateN), actionObj, playerId=playerId):
	#	return updateClient(playerId, playerName, revertN, stateN)
	#else:
	#	return Response("action not allowed", status=403, mimetype='application/json')
	gameManager.clientAction(int(revertN), int(stateN), actionObj, playerId=playerId)
	return updateClient(playerId, playerName, revertN, stateN)

@app.route("/game/<playerId>/<playerName>/game_file/<path:gameFilePath>", methods=['GET'])
def gameFile(playerId, playerName, gameFilePath):
	global gameManager
	if checkPlayerID(playerId, playerName) != None:
		flask.abort(409)
	gameFilePath = PurePath(gameFilePath)
	#print("wants to get file:", gameFilePath)
	if "." in str(gameFilePath.parent):
		flask.abort(403)
	filePath = gameManager.getFullPath(gameFilePath)
	if filePath:
		if filePath.is_file():
			#print("sending file: ", filePath)
			return send_file(str(filePath))
		else:
			flask.abort(404)
	else:
		flask.abort(403)

@app.route("/msg", methods=['GET'])
def msgPage():
	msg = flask.request.args.get('msg')
	link = flask.request.args.get('link')
	linkText = flask.request.args.get('linkText')
	return renderMsgPage(msg, link, linkText)

def renderTokenError(token):
	if token == None:
		return renderErrorPage("Missing admin token!")
	else:
		return renderErrorPage("Invalid admin token!")

@app.route("/admin", methods=['GET'])
def adminPage():
	token = flask.request.args.get('token')
	if token == settings.adminToken:
		return render_template('admin.html', gameName=_getGameName(), nPlayers=nPlayers, currentStateN=gameManager.currentStateN, adminToken=token)
	else:
		return renderTokenError(token)

@app.route("/debug", methods=['GET'])
def debugPage():
	token = flask.request.args.get('token')
	if token == settings.adminToken:
		contentHTML = createDebugPageHTML(globals(), flask.request.args.get('var'), token)
		return render_template('debug.html', gameName=_getGameName(), adminToken=token, contentHTML=contentHTML) 
	else:
		return renderTokenError(token)

@app.route("/game/revert_to/<toStateN>", methods=['GET'])
def revertGameTo(toStateN):
	token = flask.request.args.get('token')
	if token == settings.adminToken:
		toStateN = int(toStateN)
		msg = gameManager.revertToStateN(toStateN)
		return renderMsgPage(msg, "/admin?token=" + token, "return to Admin")
	else:
		return renderTokenError(token)


def newGame(gameClass, nPlayers, players={}, extraGameArgs = [], extraGameKWArgs = {}):
	gameManager = GameManager()
	game = gameClass(gameManager, *extraGameArgs, **extraGameKWArgs)
	gameManager.setGame(game)
	globals()['gameManager'] = gameManager
	globals()['nPlayers'] = nPlayers
	if 'players':
		assert(isinstance(players, dict))
		assert(len(players) <= nPlayers)
		globals()['players'] = players
	else:
		players = globals()['players']
	if enoughPlayers():
		gameManager.startGame(list(players.values()), list(players.keys())) # relying on order being the same for keys() and values()

def runServer(debug):
	global players
	print()
	print("Url for admin: http://127.0.0.1:5000/admin?token=" + settings.adminToken);
	print("Note: admin token can be set in settings.py")
	print()
	for seatN,playerName in enumerate(players.keys()):
		print("Url for player " + str(seatN) + ": http://127.0.0.1:5000/game/" + players[playerName] + "/" + playerName + "/view")
	if len(players.keys()) < nPlayers:
		print("Each new player, start at this URL: http://127.0.0.1:5000/")
	print()
	app.run(debug=debug, threaded=False, processes=1)
