

class ActionReceiver:
	"""
	Every actionReceiver instance must either contain method getName() or getDivID()
	"""

	def tryAction(self, actionArgs, playerId=None) -> bool:
		pass

def _actionObjError(text, actionObj):
	raise ValueError(text + ", actionObj = {}".format(actionObj))

def _getActionReceiver(arMap, actionReceiverID):
	if isinstance(actionReceiverID, ActionReceiver):
		return actionReceiverID
	else:
		return arMap.get(actionReceiverID, None)

def encodeActionObj(arMap, actionObj):
	if len(actionObj) == 0:
		_actionObjError("Received an empty actionObj from game (must contain actionReceiver).", actionObj)
	actionReceiver = actionObj[0] 
	if not isinstance(actionReceiver, ActionReceiver):
		_actionObjError("actionObj[0] must be an instance of ActionReceiver", actionObj)
	idMethod = getattr(actionReceiver, "getName", None)
	if not idMethod:
		idMethod = getattr(actionReceiver, "getDivID", None)
	if not idMethod:
		_actionObjError('actionReceiver (actionObj[0]) must have method "getName" or method "getDivID"', actionObj)
	actionReceiverID = idMethod()
	if not isinstance(actionReceiverID, str):
		_actionObjError('actionReceiver getName or getDivID must return a string, returned {}'.format(actionReceiverID), actionObj)
	# store actionReceiver
	arMap[actionReceiverID] = actionReceiver
	# replace actionReceiver reference with string actionReceiverID
	actionObj = (actionReceiverID,) + actionObj[1:]
	return actionObj

def encodeActionObjs(arMap, actions):
	newActions = []
	for actionObj in actions:
		newActions.append(encodeActionObj(arMap, actionObj))
	return newActions

def decodeActionObj(arMap, actionObj):
	if len(actionObj) == 0:
		raise ValueError("Received actionObj from client without an actionReceiver and no arguments!")
	actionReceiver = _getActionReceiver(arMap, actionObj[0])
	actionArgs = actionObj[1:]
	if not actionReceiver:
		raise ValueError("Received invalid actionReceiverID in actionObj, actionObj = {}".format(actionObj))
	return (actionReceiver,) + tuple(actionArgs)