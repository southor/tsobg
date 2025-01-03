
from .actions import encodeActionObj, encodeActionObjs


def _sizeToWidthHeight(size):
	""" Converts size object containing width/height numbers representing number of pixels or "auto".
	returns tuple with the two strings containing either "auto" or a number with a "px" postfix """
	x = "auto"
	y = "auto"
	if (type(size) in [tuple, list]):
		if (len(size) < 2):
			raise ValueError("pos/size property has too few elements: " + str(size))
		x = size[0]
		y = size[1]
	elif (size != "auto"):
		raise ValueError("Unknown pos/size property: " + str(size))
	return (x, y)

""" Function for converting "pos" attributes doing exactly the same as the other function """
_posToCSSLeftTop = _sizeToWidthHeight

def _deAliasUIChange(uiChange, isMutable=False):
	""" Replaces uiChange alias properties like "pos" and "size" with "left","right" and "width","height".
	If isMutable is True then the original uiChange will be altered if needed.
	If isMutale is False then a new uiChange is created if altering is needed.
	returns tuple uiChange,isOriginal where isOriginal is False if uiChange is a new object
	"""
	if uiChange[0] != "set_div":
		return uiChange, True
	opts = uiChange[2]
	hasPos = "pos" in opts
	hasSize = "size" in opts
	if not (hasPos or hasSize):
		return uiChange, True
	newOpts = opts if isMutable else opts.copy()
	if hasPos:
		left,top = _posToCSSLeftTop(newOpts.pop("pos"))
		assert(type(left) in [int, float, str])
		assert(type(top) in [int, float, str])
		newOpts["left"] = left
		newOpts["top"] = top
	if hasSize:
		width,height = _sizeToWidthHeight(newOpts.pop("size"))
		assert(type(width) in [int, float, str])
		assert(type(height) in [int, float, str])
		newOpts["width"] = width
		newOpts["height"] = height
	return ("set_div", uiChange[1], newOpts), False

def _encodeActionObjsUIChange(arMap, uiChange, isMutable):
	"""
	If isMutable is True then the original uiChange will be altered if needed.
	If isMutale is False then a new uiChnage is created if altering is needed.
	returns uiChange,isOriginal
	"""
	if uiChange[0] != "set_div":
		return uiChange, True
	opts = uiChange[2]
	onClick = opts.get("onClick", None)
	onClickActionObj = None if isinstance(onClick, str) else onClick
	actions = opts.get("actions", None)
	if not (actions or onClickActionObj):
		# For actions it will both detect no actions present (None) or actions is the empty list
		return uiChange, True
	newOpts = opts if isMutable else opts.copy()
	if onClickActionObj:
		newOpts["onClick"] = encodeActionObj(arMap, onClickActionObj)
	if actions:
		newOpts["actions"] = encodeActionObjs(arMap, actions)
	return ("set_div", uiChange[1], newOpts), False

def encodeUIChange(arMap, uiChange, isMutable=False):
	uiChange,isOriginal = _encodeActionObjsUIChange(arMap, uiChange, isMutable)
	uiChange,isOriginal = _deAliasUIChange(uiChange, isMutable or not isOriginal)
	return uiChange,isOriginal

def combineUIChanges(uiChangeA, uiChangeB):
	""" Combines the uiChanges if possible and returns the result
	If the uiChanges cannot be combined then None is returned
	uiChanges must be free of property aliases
	"""
	commandA = uiChangeA[0]
	commandB = uiChangeB[0]
	# trivial cases with nop
	if commandA == "nop":
		return uiChangeB
	elif commandB == "nop":
		return uiChangeA
	# other cases that cannot be combined unless of the same type
	if commandA not in ["set_div", "set_max_num_div_selected"]:
		raise ValueError("Unknown command: {}".format(commandA))
	if commandA != commandB:
		return None
	if commandA == "set_div":
		id = uiChangeA[1]
		if uiChangeB[1] != id:
			return None
		opts = uiChangeA[2].copy()
		opts.update(uiChangeB[2])
		return ("set_div", id, opts)
	elif commandA == "set_max_num_div_selected":
		return commandB
	else:
		assert(False) # we already made sure commandA is one of the above
		raise ValueError("Unknown command: {}".format(commandA))

class UIState():
    
	#_divOptsDefaultsEncoded = {
	divOptsDefaults = {
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
		"border":"none", # style.border
		"borderColor":"black", # style.borderColor
		# element configurations
		"parent":None, # sets parent by adding as child
		"button":None, # adds a button element with "button" as the caption and "onClick" divOpts for the event
		"img":None, # adds an img element with "img" as the img attribute
		"text":None, # adds a text element with "text" as innerHTML
		# other special
		"trapClicks":False, # If there is no onClick action and not selectable, clicks on div element can be let through to object below if trapClicks is set to False
		"selectable":False,
		"onClick":None,
		"buttonEnabled":True,
		"actions":[]
	}

	#divOptsDefaults = {
	#	**_divOptsDefaultsEncoded,
	#	"pos": "auto",
	#	"size": "auto"
	#}
		
	def __init__(self, divs = {}):
		self.maxNDivSelected = 1000
		self.divs = divs

	def __eq__(self, other):
		if isinstance(other, UIState):
			return self.divs == other.divs
		return False

	def pruneUIChange(self, uiChange):
		""" Creates a new uiChange with removed properties in uiChange that will have no effect
		uiChange must be free of property aliases
		"""
		command = uiChange[0]
		if command == "set_div":
			id = uiChange[1]
			opts = uiChange[2]
			divState = self.divs.get(id, {})
			prunedOpts = {}
			for key,value in opts.items():
				defaultValue = UIState.divOptsDefaults[key]
				valueState = divState.get(key, defaultValue)
				if value != valueState:
					prunedOpts[key] = value
			if prunedOpts == {}:
				return ("nop")
			else:
				return ("set_div", id, prunedOpts)
		elif command == "set_max_num_div_selected":
			if uiChange[1] == self.maxNDivSelected:
				return ("nop")
			else:
				return uiChange
		elif command == "nop":
			return uiChange
		else:
			raise ValueError("Unknown command: " + command)

	def uiChangeReverse(self, uiChange):
		""" returns reversed version of uiChange
		uiChange must be free of property aliases
		"""
		command = uiChange[0]
		if command == "set_div":
			id = uiChange[1]
			opts = uiChange[2]
			divState = self.divs.get(id, {})
			revOpts = {}
			for key,value in opts.items():
				if key in divState:
					revOpts[key] = divState[key]
				else:
					revOpts[key] = UIState.divOptsDefaults[key]
			if revOpts == {}:
				return ("nop")
			else:
				return ("set_div", id, revOpts)
		elif command == "set_max_num_div_selected":
			return ("set_max_num_div_selected", self.maxNDivSelected)
		elif command == "nop":
			return uiChange
		else:
			raise ValueError("Unknown command: " + command)

	def applyUIChange(self, uiChange):
		""" Returns a UIState with applied uiChange
		uiChange must be free of property aliases
		"""
		command = uiChange[0]
		if command == "set_div":
			divs = self.divs.copy()
			id = uiChange[1]
			opts = uiChange[2]
			if id in divs:
				divs[id] = {**divs[id], **opts}
			else:
				divs[id] = opts.copy()
			return UIState(divs)
		elif command == "set_max_num_div_selected":
			self.maxNDivSelected = uiChange[1]
			return self
		elif command == "nop":
			return self
		else:
			raise ValueError("Unknown command: " + command)



