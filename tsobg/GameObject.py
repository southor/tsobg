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

	def _getUIUpdateBase(self):
		parent = self._parent if self._isVisible() else None
		if isinstance(parent, GameObject):
			divOpts = {"parent":parent.getDivID(), "divPositioning":"absolute"}
		elif isinstance(parent, str):
			divOpts = {"parent":parent, "divPositioning":self._divPositioning}
		elif parent == None:
			divOpts = {"parent":None}
		else:
			raise Error("parent of {} must be either string, GameObject or None. parent={}".format(self.divID, str(parent)[:50]))
		return divOpts

	def _uiUpdateFull(self):
		divOpts = self._getUIUpdateBase()
		if divOpts["parent"] != None:
			divOpts.update(self._divProps)
			# add layout position offset
			divOpts["left"] = self.getEffectiveLeft()
			divOpts["top"] = self.getEffectiveTop()
		self._uiInterface.stageUIChange(("set_div", self._divID, divOpts))

	def _uiUpdatePos(self):
		if self._parent != None and self._isVisible():
			divOpts = {"left" : self.getEffectiveLeft(),
						"top" : self.getEffectiveTop()}
			self._uiInterface.stageUIChange(("set_div", self._divID, divOpts))

	def __init__(self, uiInterface:UIInterface, divID, **kwargs):
		self._uiInterface = uiInterface
		self._divID = divID
		self._divProps = {k:v for (k,v) in kwargs.items() if k in GameObject._propsDefaults and k not in GameObject._specialProps}
		self._parent = None
		self._flags = {"visible"}
		if "flags" in kwargs:
			self.setFlags(kwargs["flags"])
		if "pos" in kwargs:
			self.setPos(kwargs["pos"])
		if "size" in kwargs:
			self.setSize(kwargs["size"])
		self._layoutPos = ("auto", "auto")
		# _divPositioning member will automatically be used with set_div if parent is a div id, but will be ignored if parent is another GameObject (in which case absolute is used instead)
		self._divPositioning = kwargs.get("divPositioning", "static")
		self._layout = kwargs.get("layout", FreeLayout())
		parent = kwargs.get("parent", None)
		if parent:
			parent.addChild(self)
		else:
			self._uiUpdateFull()

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

	def getLayoutPos(self):
		return self._layoutPos

	def getEffectiveLeft(self):
		left = self.getLeft()
		layoutX = self._layoutPos[0]
		if left == "auto":
			return layoutX
		if layoutX == "auto":
			return left
		return left + layoutX # both of them should be numbers

	def getEffectiveTop(self):
		top = self.getTop()
		layoutY = self._layoutPos[1]
		if top == "auto":
			return layoutY
		if layoutY == "auto":
			return top
		return top + layoutY # both of them should be numbers

	def getEffectivePos(self):
		return (self.getEffectiveLeft(), self.getEffectiveTop())

	def setParent(self, parent):
		"""parent must be either a GameObject, string divID or None"""
		if self._parent is parent:
			return
		if not (isinstance(parent, GameObject) or isinstance(parent, str) or parent == None):
			raise Error("parent of {} must be either a GameObjcet, string, or None. parent={}".format(self.divID, str(parent)[:50]))
		if isinstance(self._parent, GameObject):
			self._parent.removeChild(self)
		if isinstance(parent, GameObject):
			parent.addChild(self)
		else:
			self._parent = parent
			if "visible" in self._flags:
				self._uiUpdateFull()

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
				self._uiUpdateFull()

	def setPos(self, pos):
		self.setLeft(pos[0])
		self.setTop(pos[1])
		self._uiUpdatePos()

	def setSize(self, size):
		self.setWidth(size[0])
		self.setHeight(size[1])
		self._uiUpdatePos()

	def setLayoutPos(self, layoutPos):
		self._layoutPos = layoutPos
		self._uiUpdatePos()

	# ------------ children ------------

	def hasChild(self, object):
		return self._layout.hasObject(object)

	def getChildCoordinates(self, object):
		return self._layout.getObjectCoordinates(object)

	def getFirstChild(self, remove=False):
		return self._layout.getFirstObject(remove)

	def getChildAt(self, colN, rowN):
		return self._layout.getObjectAt(colN, rowN)

	def addChild(self, object):
		if not self._layout.addObject(object):
			return False
		object._parent = self
		if "visible" in object._flags:
			object._uiUpdateFull()
		return True

	def addChildAt(self, object, colN, rowN):
		if not self._layout.addObjectAt(object, colN, rowN):
			return False
		object._parent = self
		if "visible" in object._flags:
			object._uiUpdateFull()
		return True

	def removeChild(self, object):
		if not self._layout.removeObject(object):
			return False
		object._parent = None
		if "visible" in object._flags:
			object._uiUpdateFull()
		return True

	def removeChildAt(self, object, colN, rowN):
		if not self._layout.removeObjectAt(object, colN, rowN):
			return False
		object._parent = None
		if "visible" in object._flags:
			object._uiUpdateFull()
		return True

	# ------------ visiting ------------

	def visitChildrenReduce(self, visitFunc, initRes=None):
		return self._layout.visitObjectsReduce(visitFunc, initRes)

	def visitChildrenShortcut(self, visitFunc, failRes=None):
		return self._layout.visitObjectsShortcut(visitFunc, failRes)

	# ------------ stack ------------

	def inStackOf(self, object):
		""" returns True if self is object or if self is in stack of object """
		return object.getStackCoordinatesFor(self) != None

	def getStackCoordinatesFor(self, object):
		""" returns the stack coordinates for object realtive to self (if object is self [] is returned) """
		targetObject = object
		def visitFunc(colN, rowN, object, prevRes):
			if prevRes:
				return prevRes
			res = object.getStackCoordinatesFor(targetObject)
			return [(colN, rowN)] + res if res != None else None
		if self is targetObject:
			return []
		return self.visitChildrenReduce(visitFunc, None)

	def getStackObjectAt(self, stackCoordinates: list):
		if len(stackCoordinates) == 0:
			return self
		coords = stackCoordinates[0]
		child = self.getChildAt(*coords) if coords else self.getFirstChild()
		if child:
			return child.getStackObjectAt(stackCoordinates[1:])
		return None


		
			


# Add new methods to GameObject based on divOpts
GameObject._setupDivProps(UIState.divOptsDefaults)