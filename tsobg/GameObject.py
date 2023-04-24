from .UIInterface import UIInterface
from .FreeLayout import FreeLayout
from .UIState import UIState


class GameObject():

	_specialProps = {"parent", "divPositioning"}

	def _createGetMethod(key):
		def _methodTemplate(self):
			return self._divProps[key] if key in self._divProps else GameObject._propsDefaults[key]
		return _methodTemplate

	def _createSetMethod(key):
		def _methodTemplate(self, val):
			self._divProps[key] = val
			if self._isVisible():
				self._uiInterface.stageUIChange(("set_div", self._divID, {key:val}))
		return _methodTemplate

	def _setupDivProps(propsDefaults: dict):
		# add the default values
		GameObject._propsDefaults = propsDefaults
		# add getter methods
		for p in propsDefaults:
			name = p[0].upper() + p[1:]
			if p not in GameObject._specialProps:
				setattr(GameObject, "get" + name, GameObject._createGetMethod(p))
				setattr(GameObject, "set" + name, GameObject._createSetMethod(p))

	def _isVisible(self):
		return self._parent and "visible" in self._flags

	def _uiUpdate(self):
		parent = self._parent if self._isVisible() else None
		if isinstance(parent, GameObject):
			divOpts = {"parent":parent.getDivID(), "divPositioning":"absolute"}
		elif isinstance(parent, str):
			divOpts = {"parent":parent, "divPositioning":self._divPositioning}
		elif parent == None:
			divOpts = {"parent":None}
		else:
			raise Error("parent of {} must be either string, GameObject or None. parent={}".format(self.divID, str(parent)[:50]))
		if parent != None:
			#selectable = self.getFlag("selectable")
			#trapClicks = self.getFlag("trapClicks")
			#divOpts.update({"pos":self._uiPos, "size":self._uiSize, "text":self._text, "img":self._image, "color":self._color, "border":self._border, "borderColor":self._borderColor, "trapClicks":trapClicks, "selectable":selectable, "onClick":self._onClick, "actions":self._actions})
			divOpts.update(self._divProps)
		self._uiInterface.stageUIChange(("set_div", self._divID, divOpts))

	def __init__(self, uiInterface:UIInterface, divID, **kwargs):
		self._uiInterface = uiInterface
		self._divID = divID
		self._divProps = {k:v for (k,v) in kwargs.items() if k in GameObject._propsDefaults and k not in GameObject._specialProps}
		self._parent = None
		#self._flags = {"visible", "trapClicks"}
		self._flags = {"visible"}
		if "flags" in kwargs:
			self.setFlags(kwargs["flags"])
		if "pos" in kwargs:
			self.setPos(kwargs["pos"])
		if "size" in kwargs:
			self.setSize(kwargs["size"])
		# _divPositioning member will automatically be used with set_div if parent is a div id, but will be ignored if parent is another GameObject (in which case absolute is used instead)
		self._divPositioning = kwargs.get("divPositioning", "static")
		self._layout = kwargs.get("layout", FreeLayout())
		#self._uiPos = kwargs.get("uiPos", "auto") # passed uiPos will not be used if parent is provided and parent uses GridLayout
		#self._uiSize = kwargs.get("uiSize", "auto")
		#self._text = kwargs.get("text", None)
		#self._image = kwargs.get("image", None)
		#self._color = kwargs.get("color", "transparent")
		#self._border = kwargs.get("border", "none")
		#self._borderColor = kwargs.get("borderColor", "black")
		#self._onClick = kwargs.get("onClick", None)
		#self._actions = kwargs.get("actions", [])
		parent = kwargs.get("parent", None)
		if parent:
			if isinstance(self._layout, FreeLayout):
				#parent.putObject(self, self._uiPos)
				parent.putObject(self, self.getPos())
			else:
				parent.putObject(self)
		else:
			self._uiUpdate()

	def getDivID(self):
		return self._divID

	def getParent(self):
		return self._parent

	def getLayoutType(self):
		return type(self._layout)

	def getFlags(self):
		return self._flags

	def getFlag(self, flag):
		return flag in self._flags

	def getPos(self):
		return (self.getLeft(), self.getTop())

	def getSize(self):
		return (self.getWidth(), self.getHeight())

	#def getUIPos(self):
	#	return self._uiPos

	#def getUISize(self):
	#	return self._uiSize

	#def getText(self):
	#	return self._text

	#def getImage(self):
	#	return self._image

	#def getColor(self):
	#	return self._color
	
	#def getBorder(self):
	#	return self._border

	#def getBorderColor(self):
	#	return self._borderColor

	#def getOnClick(self):
	#	return self._onClick

	#def getActions(self):
	#	return self._actions


	def setParent(self, parent):
		"""parent must be either a GameObject, string divID or None"""
		if self._parent is parent:
			return
		if not (isinstance(parent, GameObject) or isinstance(parent, str) or parent == None):
			raise Error("parent of {} must be either a GameObjcet, string, or None. parent={}".format(self.divID, str(parent)[:50]))
		if isinstance(self._parent, GameObject):
			self._parent.removeObject(self)
		if isinstance(parent, GameObject):
			parent.putObject(self)
		else:
			self._parent = parent
			if "visible" in self._flags:
				self._uiUpdate()

	def setFlags(self, *argsFlags, **kwargFlags):
		"""
		Is used to turn on, off a flag, or replace all flag statuses with new ones.
		Arguments will be processed in the order they appear. kwargsFlags will be processed last.
		Process starts with the current flags status of the gameObject.
		For every arg in argsFlags:
			If it is a string: The flag is turned on.
			If it is a dictionary: Each key must be a string, the value will be turned into a boolean and used to set or unset the flag.
			If it is a none dictionary iterable: Every member must be a string flag name. First all flags are set to off and then for every flag in the iterable that flag is turned on.
		kwargsFlags:
			Each key must be a string, the value will be turned into a boolean and used to set or unset the flag.
		"""
		flags = self._flags.copy()

		def processDictionary(d):
			for flag,val in arg.items():
				if not isinstance(flag, str):
					raise RuntimeError("setFlags dictionary argument must only contain strings (flag names) as keys, flag={}".format(flag))
				if val:
					flags.add(flag)
				else:
					flags.discard(flag)

		inputArgs = argsFlags + (kwargFlags,)
		for arg in inputArgs:
			# check for string
			if isinstance(arg, str):
				flags.add(arg)
				continue
			# check for dictionary
			if(isinstance(arg, dict)):
				processDictionary(arg)
				continue
			# check for iterable
			try:
				flags2 = set()
				for flag in arg:
					if not isinstance(flag, str):
						raise RuntimeError("setFlags iterable argument must only contain strings (flag names), flag={}".format(flag))
					flags2.add(flag)
				# since for loop did not trigger exception we know arg is an iterable, we can update the flags
				flags = flags2
			except TypeError as e:
				raise RuntimeError("setFlags argument must be either a string, dictionary, or iterable: {}".format(arg))
		if flags != self._flags:
			self._flags = flags
			if self._parent:
				# TODO: Add optional argument to _uiChange so we can tell it to only update flags (for performance)
				self._uiUpdate()

	def setPos(self, pos):
		self.setLeft(pos[0])
		self.setTop(pos[1])

	def setSize(self, size):
		self.setWidth(size[0])
		self.setHeight(size[1])

	#def setUIPos(self, uiPos):
	#	if self._uiPos == uiPos:
	#		return
	#	self._uiPos = uiPos
	#	if self._isVisible():
	#		self._uiInterface.stageUIChange(("set_div", self._divID, {"pos":uiPos}))

	#def setUISize(self, uiSize):
	#	if self._uiSize == uiSize:
	#		return
	#	self._uiSize = uiSize
	#	if self._isVisible():
	#		self._uiInterface.stageUIChange(("set_div", self._divID, {"size":uiSize}))

	#def setText(self, text):
	#	self._text = text
	#	if self._isVisible():
	#		self._uiInterface.stageUIChange(("set_div", self._divID, {"text":text}))

	#def setImage(self, filename):
	#	self._image = filename
	#	if self._isVisible():
	#		self._uiInterface.stageUIChange(("set_div", self._divID, {"img":filename}))

	#def setColor(self, color):
	#	self._color = color
	#	if self._isVisible():
	#		self._uiInterface.stageUIChange(("set_div", self._divID, {"color":color}))

	#def setBorder(self, border):
	#	self._border = border
	#	if self._isVisible():
	#		self._uiInterface.stageUIChange(("set_div", self._divID, {"border":border}))

	#def setBorderColor(self, borderColor):
	#	self._borderColor = borderColor
	#	if self._isVisible():
	#		self._uiInterface.stageUIChange(("set_div", self._divID, {"borderColor":borderColor}))

	#def setOnClick(self, onClick):
	#	self._onClick = onClick
	#	if self._parent:
	#		self._uiInterface.stageUIChange(("set_div", self._divID, {"onClick":onClick}))

	#def setActions(self, actions):
	#	self._actions = actions
	#	if self._parent:
	#		self._uiInterface.stageUIChange(("set_div", self._divID, {"actions":actions}))

	# ------------ children ------------

	def getObject(self, *layoutArgs):
		return self._layout.getObject(*layoutArgs)

	def getObjectLayoutArgs(self, object, recursive=False):
		return self._layout.getObjectLayoutArgs(object, recursive)

	def putObject(self, object, *layoutArgs):
		if not self._layout.addObject(object, *layoutArgs):
			return False
		object._parent = self
		if "visible" in object._flags:
			object._uiUpdate()
		return True

	def hasObject(self, object, recursive=False, remove=False):
		"""
		Returns true if object is child or any child "has object"
		"""
		if self._layout.hasObject(object, recursive=recursive, remove=remove):
			if remove:
				if object._parent is self:
					object._parent = None
					if "visible" in object._flags:
						object._uiUpdate()
				else:
					# The parent of object must be a child or descendent, so it should already have been removed by call to self._layout.hasObject
					assert(object._parent is None)
			return True
		return False

	def removeObject(self, object, recursive=False):
		return self.hasObject(object, recursive=recursive, remove=True)

# Add new methods to GameObject based on divOpts
GameObject._setupDivProps(UIState.divOptsDefaults)