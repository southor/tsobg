
divOptsDefaults = {"parent":None, "pos":"auto", "size":"auto", "img":None, "border":None, "color":"transparent"}

uiStartState = { "divs": {} }


def updateUIChange(uiChange, uiChangeOther):
	""" Updates uiChange with uiChangeOther (combines)
	returns False if uiChanges cannot be combined
	"""
	if uiChange[0] == "set_div":
		if uiChangeOther[0] == "set_div":
			if uiChange[1] != uiChangeOther[1]:
				return False # div id differs
			uiChange[2].update(uiChangeOther[2])
			return True
		if uiChangeOther[0] == "nop":
			return True
	return False

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
			valueState = divState.get(key, divOptsDefaults[key])
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
				revOpts[key] = divOptsDefaults[key]
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
