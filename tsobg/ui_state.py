
#__divOptsDefaults = {"divPositioning":"static", "parent":None, "class":None, "pos":"auto", "size":"auto", "img":None, "border":None, "color":"transparent", "text":None, "actions":[]}
__divOptsDefaults = {
	# css properties
	"class":None,
	"divPositioning":"static", # style.position
	
	# css positioning properties, number valeus will be converted to strings with "px" attached
	"left":"auto",
	"top":"auto",
	"right":"auto",
	"bottom":"auto",
	"width":"auto",
	"height":"auto",
	
	"color":"transparent", # style.backgroundColor
	"border":None, # style.border
	# element configurations
	"parent":None, # sets parent by adding as child
	"img":None, # adds an img element with "img" as the img attribute
	"text":None, # adds a text element with "text" as innerHTML
	# other special
	"actions":[] # does not change the style, specifies interactability
	}

def getUIStartState():
	return { "divs": {} }


def sizeToCSSpxComponents(size):
	""" Converts size object containing width/height numbers representing number of pixels or "auto".
    returns tuple with the two strings containing either "auto" or a number with a "px" postfix """
	x = "auto"
	y = "auto"
	if (type(size) in [tuple, list]):
		if (len(size) < 2):
			raise RuntimeError("pos/size property has too few elements: " + str(size))
		x = size[0]
		y = size[1]
	elif (size != "auto"):
		raise RuntimeError("Unknown pos/size property: " + str(size))
	return (x, y)

""" Function for converting "pos" attributes doing exactly the same as the other function """
posToCSSpxComponents = sizeToCSSpxComponents

def deAliasUIChange(uiChange):
	""" Replaces uiChange alias properties like "pos" and "size" with "left","right" and "width","height".
	Either returns the modified uiChange or the original if not modifications needed"""
	if uiChange[0] != "set_div":
		return uiChange
	opts = uiChange[2]
	hasPos = "pos" in opts
	hasSize = "size" in opts
	if not (hasPos or hasSize):
		return uiChange
	newOpts = opts.copy()
	if hasPos:
		left,top = posToCSSpxComponents(newOpts.pop("pos"))
		newOpts["left"] = left
		newOpts["top"] = top
	if hasSize:
		width,height = sizeToCSSpxComponents(newOpts.pop("size"))
		newOpts["width"] = width
		newOpts["height"] = height
	return ("set_div", uiChange[1], newOpts)


def combineUIChanges(uiChangeA, uiChangeB):
	""" Combines the uiChanges if possible and returns the result
	If the uiChanges cannot be combined then None is returned
	uiChanges must be free of property alias
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


def pruneUIChange(uiState, uiChange):
	""" Creates a new uiChange with removed properties in uiChange that will have no effect
	uiChange must be free of property alias
	"""
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

def uiChangeReverse(uiState, uiChange):
	""" returns reversed version of uiChange
	uiChange must be free of property alias
	"""
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

def applyUIChange(uiState, uiChange):
	""" modifies uiState with uiChange 
	uiChange must be free of property alias
	"""
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
