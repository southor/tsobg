

divOptsDefaults = {"parent":None, "pos":"auto", "size":"auto", "img":None, "border":None, "color":"transparent"}

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
		return ("set_div", id, prunedOpts)
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
		return ("set_div", id, revOpts)
	else:
		raise RuntimeException("Unknown command: " + command)
	
# modifies uiState with uiChange
def applyUIChange(uiState, uiChange):
	stateDivs = uiState["divs"]
	command = uiChange[0]
	if command == "set_div":
		id = uiChange[1]
		opts = uiChange[2]
		if id not in stateDivs:
			stateDivs[id] = opts
		else:
			stateDivs[id].update(opts)
	else:
		raise RuntimeException("Unknown command: " + command)
	


uiStartState = { "divs": {} }