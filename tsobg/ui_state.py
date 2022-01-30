
__divOptsDefaults = {"divPositioning":"static", "parent":None, "class":None, "pos":"auto", "size":"auto", "img":None, "border":None, "color":"transparent", "text":None, "actions":[]}

#uiStartState = { "divs": {} }

def getUIStartState():
	return { "divs": {} }


def combineUIChanges(uiChangeA, uiChangeB):
	""" Combines the uiChanges if possible and returns the result
	If the uiChanges cannot be combined then None is returned
	"""
	commandA = uiChangeA[0]
	commandB = uiChangeB[0]
	if commandA == "set_div":
		if commandB == "set_div":
			id = uiChangeA[1]
			if uiChangeB[1] != id:
				return None
			opts = uiChangeA[2].copy()
			opts.update(uiChangeB[2])
			return ("set_div", id, opts)
		elif commandB == "nop":
			return uiChangeA
		else:
			raise RuntimeException("Unknown command: " + commandB)
	elif commandA == "nop":
		return uiChangeB
	else:
		raise RuntimeException("Unknown command: " + commandA)

# returns pruned uiChange 
def pruneUIChange(uiState, uiChange):
	stateDivs = uiState["divs"]
	command = uiChange[0]
	if command == "set_div":
		id = uiChange[1]
		opts = uiChange[2]
		divState = stateDivs.get(id, {})
		prunedOpts = {}
		for key,value in opts.items():
			valueState = divState.get(key, __divOptsDefaults[key])
			if value != valueState:
				prunedOpts[key] = value
		if prunedOpts == {}:
			return ("nop")
		else:
			return ("set_div", id, prunedOpts)
	elif command == "nop":
		return uiChange
	else:
		raise RuntimeException("Unknown command: " + command)

# returns reversed version of uiChange 
def uiChangeReverse(uiState, uiChange):
	stateDivs = uiState["divs"]
	command = uiChange[0]
	if command == "set_div":
		id = uiChange[1]
		opts = uiChange[2]
		divState = stateDivs.get(id, {})
		revOpts = {}
		for key,value in opts.items():
			if key in divState:
				revOpts[key] = divState[key]
			else:
				revOpts[key] = __divOptsDefaults[key]
		if revOpts == {}:
			return ("nop")
		else:
			return ("set_div", id, revOpts)
	elif command == "nop":
		return uiChange
	else:
		raise RuntimeException("Unknown command: " + command)
	
# modifies uiState with uiChange
def applyUIChange(uiState, uiChange):
	stateDivs = uiState["divs"]
	command = uiChange[0]
	if command == "set_div":
		id = uiChange[1]
		opts = uiChange[2]
		if id in stateDivs:
			stateDivs[id].update(opts)
		else:
			stateDivs[id] = opts.copy()
	elif command == "nop":
		return
	else:
		raise RuntimeException("Unknown command: " + command)
