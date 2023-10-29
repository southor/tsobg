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
		# _divPositioning member will automatically be used with set_div if parent is a divID, but will be ignored if parent is another GameObject (in which case absolute is used instead)
		self._divPositioning = kwargs.get("divPositioning", "static")
		self._childrenLayout = kwargs.get("childrenLayout", FreeLayout())
		parent = kwargs.get("parent", None)
		if parent:
			self.setParent(parent)
		else:
			self._uiUpdateFull()

	def getDivID(self):
		return self._divID

	def getParent(self):
		return self._parent

	def getChildrenLayoutType(self):
		return type(self._childrenLayout)

	def getLayoutPos(self):
		""" Returns the position as set by the parents childrenLayout object. """
		return self._layoutPos

	def getFlags(self):
		return self._flags

	def getFlag(self, flag):
		return flag in self._flags

	def getPos(self):
		return (self.getLeft(), self.getTop())

	def getSize(self):
		return (self.getWidth(), self.getHeight())

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

	def setParent(self, parent, place=None, allowReplace=True):
		"""parent must be either a GameObject, string divID or None"""
		if self._parent is parent:
			return
		if not (isinstance(parent, GameObject) or isinstance(parent, str) or parent == None):
			raise TypeError("parent of {} must be either a GameObjcet, string, or None. parent={}".format(self.divID, str(parent)[:50]))
		if isinstance(self._parent, GameObject):
			self._parent.removeChild(self)
		assert(self._parent == None)
		if isinstance(parent, GameObject):
			if place:
				parent.setChildAt(place, self, allowReplace)
			else:
				parent.addChild(self)
		else:
			assert(isinstance(parent, str))
			self._parent = parent
			if "visible" in self._flags:
				self._uiUpdateFull()

	def setLayoutPos(self, layoutPos):
		""" Used by the parents childrenLayout object to set the position based on the layout. """
		self._layoutPos = layoutPos
		self._uiUpdatePos()

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

	# ------------ children ------------

	def getNRows(self):
		return self._childrenLayout.getNRows()

	def getNColumns(self):
		return self._childrenLayout.getNColumns()

	def getGridSize(self):
		return self._childrenLayout.getGridSize()

	def getNChildren(self):
		return self._childrenLayout.getNObjects()

	def hasChild(self, arg):
		""" arg can be either GameObject or divID (str) """
		if isinstance(arg, GameObject):
			object = arg
		elif isinstance(arg, str):
			object = self.getChild(arg)
			return bool(object)
		else:
			raise TypeError('"arg" argument passed to hasChild must be a GameObject or a string divID, child=' + str(arg))
		res = object._parent is self
		if res:
			assert(self._childrenLayout.hasObject(object))
		else:
			assert(not self._childrenLayout.hasObject(object))
		return res

	def getChildPlace(self, arg):
		""" param arg can be either GameObject or divID (str) """
		if isinstance(arg, GameObject):
			object = arg
		elif isinstance(arg, str):
			object = self.getChild(arg)
			if not object:
				return None
		else:
			raise TypeError('"arg" argument passed to getChildPlace must be a GameObject or a string divID, child=' + str(arg))
		return self._childrenLayout.getObjectPlace(object)

	def getFirstChild(self, remove=False):
		object = self._childrenLayout.getFirstObject(remove)
		if object and remove:
			object._parent = None
			if "visible" in object._flags:
				object._uiUpdateFull()
		return object

	def getChild(self, divID):
		""" get child by divID, returns child GameObject or None """
		return self.visitChildrenShortcut(lambda place, child: child if child.getDivID() == divID else None)

	def getChildAt(self, place):
		return self._childrenLayout.getObjectAt(place)

	def getAllChildren(self):
		return self._childrenLayout.getAllObjects()

	def getAllChildrenWithPlace(self):
		return self._childrenLayout.getAllObjectsPlaceTuple()

	def addChild(self, object):
		if not isinstance(object, GameObject):
			raise TypeError("Child to add must be a GameObject, child=" + str(object))
		if object._parent:
			raise ValueError("Object must not already have a parent when being added to a parent.")
		if not self._childrenLayout.addObject(object):
			return False
		object._parent = self
		if "visible" in object._flags:
			object._uiUpdateFull()
		return True

	def addChildAt(self, place, object):
		if not isinstance(object, GameObject):
			raise TypeError("Child to add must be a GameObject, child=" + str(object))
		res,prevChild = self.setChildAt(place, object, allowReplace=False)
		assert(prevChild == None)
		return res

	def setChildAt(self, place, object, allowReplace=True): 
		if not (object == None or isinstance(object, GameObject)):
			raise TypeError("Object passed to setChildAt must be either a None or a GameObject, child=" + str(object))
		if object and object._parent:
			raise ValueError("Object passed to setChildAt must not already have a parent.")
		res,prevObject = self._childrenLayout.setObjectAt(place, object, allowReplace)
		if prevObject:
			prevObject._parent = None
			if "visible" in prevObject._flags:
				prevObject._uiUpdateFull()
		if res and object:
			object._parent = self
			if "visible" in object._flags:
				object._uiUpdateFull()
		return res,prevObject

	def removeChild(self, arg):
		""" param arg can be either GameObject or divID (str) """
		if isinstance(arg, GameObject):
			object = arg
		elif isinstance(arg, str):
			object = self.getChild(arg)
			if not object:
				return False
		else:
			raise TypeError('"arg" argument passed to removeChild must be a GameObject or a string divID, child=' + str(arg))
		if not self._childrenLayout.removeObject(object):
			return False
		object._parent = None
		if "visible" in object._flags:
			object._uiUpdateFull()
		return True

	def removeChildAt(self, place):
		""" returns the object that was removed, otherwise None """
		object = self._childrenLayout.removeObjectAt(place)
		if object:
			object._parent = None
			if "visible" in object._flags:
				object._uiUpdateFull()
		return object

	def removeAllChildren(self, visitFunc=None):
		"""
		Calls visitFunc(place, object) for each removed child (if visitFunc is non-None)
		returns number of children removed
		"""
		return self._childrenLayout.removeAllObjects(visitFunc=visitFunc)

	# ------------ visiting ------------

	def visitChildren(self, visitFunc):
		return self._childrenLayout.visitObjectsReduce(lambda place, object, prevRes: visitFunc(place, object))

	def visitChildrenReduce(self, visitFunc, initRes=None):
		return self._childrenLayout.visitObjectsReduce(visitFunc, initRes)

	def visitChildrenShortcut(self, visitFunc, failRes=None):
		return self._childrenLayout.visitObjectsShortcut(visitFunc, failRes)

	# ------------ stack ------------

	def inStackOf(self, arg) -> bool:
		"""
		Parameter arg must be a GameObject or the divID of the GameObject
		returns True if self is the object or if self is in stack of the object
		"""
		if (self is arg) or (self.getDivID() == arg):
			return True
		if isinstance(self._parent, GameObject):
			return self._parent.inStackOf(arg)
		if isinstance(arg, GameObject) or isinstance(arg, str):
			return arg == self._parent
		else:
			raise TypeError('"arg" argument passed to removeChild must be a GameObject or a string divID, child=' + str(arg))

	def getStackCoordinatesFor(self, arg):
		"""
		Parameter arg can either be a GameObject or the divID of the GameObject
		returns the stack coordinates for the object realtive to self (if the object is self then [] is returned)
		"""
		if self is arg or self.getDivID() == arg:
			return []
		def visitFunc(place, child, prevRes):
			if prevRes:
				return prevRes
			res = child.getStackCoordinatesFor(arg)
			return [place] + res if res != None else None
		return self.visitChildrenReduce(visitFunc, None)

	def getStackObject(self, divID):
		if self.getDivID() == divID:
			return self
		return self.visitChildrenShortcut(lambda place, child: child.getStackObject(divID))

	def getStackObjectAt(self, stackCoordinates: list):
		if len(stackCoordinates) == 0:
			return self
		place = stackCoordinates[0]
		child = self.getChildAt(place) if place else self.getFirstChild()
		if child:
			return child.getStackObjectAt(stackCoordinates[1:])
		return None


# Add new methods to GameObject based on divOpts
GameObject._setupDivProps(UIState.divOptsDefaults)