

class ActionReceiver:
	"""
	Every actionReceiver instance must either contain method getName() or getDivID()
	"""

	def tryAction(self, *args, **kwargs) -> bool:
		return False

def _raiseActionObjError(text, actionObj):
	raise ValueError(text + ", actionObj = {}".format(actionObj))


def encodeActionObj(arMap, actionObj):
	"""
	arMap stores actionReceiver of type ActionReceiver by actionReceiverID of type string
	actionObj should be a dictionary with the key "receiver" and optionally the keys "args", "kwargs"
	actionReceiver can either be a string actionReceiverID, or of type ActionReceiver
	"""
	
	def checkGetActionObjMemberType(actionObj, name, type1, type2, typesStr):
		val = actionObj.get(name, None)
		#if (val is not None) or mandatoryMember:
		if not (isinstance(val, type1) or isinstance(val, type2)):
			_raiseactionObjError('actionObj must have a member "{}" and instance of {}'.format(name, typesStr), actionObj)
		return val
	
	def checkArg(val, categoryName, allowedLookup):
		if isinstance(val, str) and val[:1] == "$" and val not in allowedLookups:
			if allowedLookup:
				_raiseactionObjError('actionObj {0} member contains an unknown $-lookupName "{1}", only lookups from the list {2} are allowed.'.format(categoryName, val, allowedLookups), actionObj)
			else:
				_raiseactionObjError('actionObj {0} member contains a $-lookup "{1}", lookups are not allowed in {0}.'.format(categoryName, val), actionObj)
	
	# check actionObj type
	if not isinstance(actionObj, dict):
		_raiseactionObjError("actionObj must be of type dict", actionObj)
	
	# check for unknown actionObj members
	allowedKeys = ["receiver", "args", "kwargs"]
	for key in actionObj:
		if key not in allowedKeys:
			_raiseactionObjError("actionObj contains an unknown key, only keys from the list {} are allowed".format(allowedKeys), actionObj)
	
	# check that actionObj members are correct
	actionObj = {"args":[], "kwargs":{}, **actionObj} # add args and kwargs if it is not already there
	actionReceiver = checkGetActionObjMemberType(actionObj, "receiver", str, ActionReceiver, "ActionReceiver or a string representing actionReceiverID")
	args = checkGetActionObjMemberType(actionObj, "args", tuple, list, "tuple or list")
	kwargs = checkGetActionObjMemberType(actionObj, "kwargs", dict, dict, "dict")
	
	# check for unknown lookups in actionObj args
	allowedLookups = ["$playerId", "$divId", "$isSelected", "$allSelected"]
	for val in args:
		checkArg(val, "args", allowedLookups)
	# check for lookups in actionObj kwargs (not allowed)
	for key,val in kwargs:
		checkArg(val, "kwargs", [])

	# perform encoding (replace ActionReceiver with actionReceiverID)
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

	# return result
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