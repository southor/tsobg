

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

def deAliasUIChange(uiChange, isMutable=False):
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
		left,top = posToCSSpxComponents(newOpts.pop("pos"))
		assert(type(left) in [int, float, str])
		assert(type(top) in [int, float, str])
		newOpts["left"] = left
		newOpts["top"] = top
	if hasSize:
		width,height = sizeToCSSpxComponents(newOpts.pop("size"))
		assert(type(width) in [int, float, str])
		assert(type(height) in [int, float, str])
		newOpts["width"] = width
		newOpts["height"] = height
	return ("set_div", uiChange[1], newOpts), False

def combineUIChanges(uiChangeA, uiChangeB):
	""" Combines the uiChanges if possible and returns the result
	If the uiChanges cannot be combined then None is returned
	uiChanges must be free of property aliases
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
			raise RuntimeError("Unknown command: {}".format(commandB))
	elif commandA == "nop":
		return uiChangeB
	else:
		raise RuntimeException("Unknown command: {}".format(commandA))

class UIState():
    
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
		"border":None, # style.border
		# element configurations
		"parent":None, # sets parent by adding as child
		"img":None, # adds an img element with "img" as the img attribute
		"text":None, # adds a text element with "text" as innerHTML
		# other special
		"actions":[], # specifies interactability for the div
		"imgActions":[] # specifies interactability for the div image
		}
		
	def __init__(self, divs = {}):
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
				valueState = divState.get(key, UIState.divOptsDefaults[key])
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
		elif command == "nop":
			return uiChange
		else:
			raise RuntimeException("Unknown command: " + command)

	def applyUIChange(self, uiChange):
		""" Creates a new UIState with applied uiChange and returns the result 
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
		elif command == "nop":
			return self
		else:
			raise RuntimeException("Unknown command: " + command)



