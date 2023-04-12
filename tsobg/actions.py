

class ActionReceiver:
	"""
	Every actionReceiver instance must either contain method getName() or getDivID()
	"""

	def tryAction(self, actionArgs, playerId) -> bool:
		return False

def _raiseActionObjError(text, actionObj):
	raise ValueError(text + ", actionObj = {}".format(actionObj))


def encodeActionObj(arMap, actionObj):
	"""
	arMap stores actionReceiver of type ActionReceiver by actionReceiverID of type string
	actionObj should be a dictionary with the key "receiver" and optionally the keys "args", "kwargs"
	actionReceiver can either be a string actionReceiverID, or of type ActionReceiver
	"""
	
	def checkGetActionObjMemberType(actionObj, name, type1, type2, typesStr, mandatoryMember):
		val = actionObj.get(name, None)
		if (val is not None) or mandatoryMember:
			if not (isinstance(val, type1) or isinstance(val, type2)):
				_raiseactionObjError('actionObj must have a member "{}" and instance of {}'.format(name, typesStr), actionObj)
		return val
	
	if not isinstance(actionObj, dict):
		_raiseactionObjError("actionObj must be of type dict", actionObj)
	allowedKeys = ["receiver", "args", "kwargs"]
	for key in actionObj:
		if key not in allowedKeys:
			_raiseactionObjError("actionObj contains an unknown key, only keys from the list {} are allowed".format(allowedKeys), actionObj)
	actionReceiver = actionObj.get("receiver", None)
	checkGetActionObjMemberType(actionObj, "receiver", str, ActionReceiver, "ActionReceiver or a string representing actionReceiverID", True)
	checkGetActionObjMemberType(actionObj, "args", tuple, list, "tuple or list", False)
	checkGetActionObjMemberType(actionObj, "kwargs", dict, dict, "dict", False)
	if isinstance(actionReceiver, ActionReceiver):
		idMethod = getattr(actionReceiver, "getName", None)
		if not idMethod:
			idMethod = getattr(actionReceiver, "getDivID", None)
		if not idMethod:
			_raiseactionObjError('actionReceiver must have method "getName" or method "getDivID"', actionObj)
		actionReceiverID = idMethod()
		if not isinstance(actionReceiverID, str):
			_actionObjError('actionReceiver getName or getDivID method must return a string, returned {}'.format(actionReceiverID), actionObj)
		# store actionReceiver
		arMap[actionReceiverID] = actionReceiver
		# replace actionReceiver reference with string actionReceiverID
		actionObj = {**actionObj, "receiver":actionReceiverID}
	else:
		assert(isinstance(actionReceiver, str))
	return actionObj

def encodeActionObjs(arMap, actionObjs):
	newActionObjs = []
	for actionObj in newActionObjs:
		newActions.append(encodeactionObj(arMap, actionObj))
	return newActionObjs

def decodeActionReceiver(arMap, actionReceiver):
	if isinstance(actionReceiver, ActionReceiver):
		return actionReceiver
	if not isinstance(actionReceiver, str):
		raise ValueError("actionReceiver sent by client must be a string, actionReceiver = {}".format(actionReceiver))
	if actionReceiver not in arMap:
		raise ValueError("No actionReceiver registered for actionRecieverID sent by client, actionReceiver = {}".format(actionReceiver))
	return arMap[actionReceiver]