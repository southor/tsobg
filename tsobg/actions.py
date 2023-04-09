

class ActionReceiver:
	"""
	Every actionReceiver instance must either contain method getName() or getDivID()
	"""

	def tryAction(self, actionArgs, playerId) -> bool:
		pass

def _raiseActionObjError(text, actionObj):
	raise ValueError(text + ", actionObj = {}".format(actionObj))

#def _getActionReceiver(arMap, actionReceiverID):
#	if isinstance(actionReceiverID, ActionReceiver):
#		return actionReceiverID
#	elif isinstance(actionReceiverID, str):
#		return arMap.get(actionReceiverID, None)
#	else:
#		return None

def encodeActionObj(arMap, actionObj):
	"""
	arMap stores actionReceiver of type ActionReceiver by actionReceiverID of type string
	actionObj should be a tuple on the form (actionReceiver, *actionArgs)
	actionReceiver can either be a string actionReceiverID, or of type ActionReceiver
	"""
	if not isinstance(actionObj, tuple):
		_raiseActionObjError("actionObj must be of type tuple", actionObj)
	if len(actionObj) == 0:
		_raiseActionObjError("Received an empty actionObj from game (must contain actionReceiver)", actionObj)
	actionReceiver = actionObj[0]
	if not (isinstance(actionReceiver, str) or isinstance(actionReceiver, ActionReceiver)):
		_raiseActionObjError("actionObj[0] must be an instance of ActionReceiver or a string actionReceiverID", actionObj)
	if isinstance(actionReceiver, ActionReceiver):
		idMethod = getattr(actionReceiver, "getName", None)
		if not idMethod:
			idMethod = getattr(actionReceiver, "getDivID", None)
		if not idMethod:
			_raiseActionObjError('actionReceiver (actionObj[0]) must have method "getName" or method "getDivID"', actionObj)
		actionReceiverID = idMethod()
		if not isinstance(actionReceiverID, str):
			_actionObjError('actionReceiver getName or getDivID method must return a string, returned {}'.format(actionReceiverID), actionObj)
		# store actionReceiver
		arMap[actionReceiverID] = actionReceiver
		# replace actionReceiver reference with string actionReceiverID
		actionObj = (actionReceiverID,) + actionObj[1:]
	else:
		assert(isinstance(actionReceiver, str))
	return actionObj

def encodeActionObjs(arMap, actions):
	newActions = []
	for actionObj in actions:
		newActions.append(encodeActionObj(arMap, actionObj))
	return newActions

def decodeActionReceiver(arMap, actionReceiver):
	if isinstance(actionReceiver, ActionReceiver):
		return actionReceiver
	if not isinstance(actionReceiver, str):
		raise ValueError("actionReceiver sent by client must be a string, actionReceiver = {}".format(actionReceiver))
	if actionReceiver not in arMap:
		raise ValueError("No actionReceiver registered for actionRecieverID sent by client, actionReceiver = {}".format(actionReceiver))
	return arMap[actionReceiver]

#def decodeActionObj(arMap, actionObj):
#	if type(actionObj) not in [tuple, list]:
#		_raiseActionObjError("Client actionObj must be of type tuple or list", actionObj)
#	if len(actionObj) == 0:
#		_raiseActionObjError("Client actionObj is empty", actionObj)
#	actionReceiver = actionObj[0]
#	actionArgs = actionObj[1:]
#	if not isinstance(actionReceiver, str):
#		_raiseActionObjError("actionReceiver sent by client must be a string", actionObj)
#	if actionReceiverID not in arMap:
#		_raiseActionObjError("No actionReceiver registered for actionRecieverID sent by client", actionObj)
#	actionReceiver = arMap[actionReceiverID]
#	assert(isinstance(actionReceiver, ActionReceiver))
#	return (actionReceiver,) + tuple(actionArgs)