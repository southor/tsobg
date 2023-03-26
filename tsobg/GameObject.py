from .UIInterface import UIInterface
from .FreeLayout import FreeLayout


class GameObject():

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
			#selectable = ("selectable" in self._flags)
			#divOpts.update({"pos":self._uiPos, "size":self._uiSize, "text":self._text, "img":self._image, "border":self._border, "actions":self._actions, "selectable":selectable})
			divOpts.update({"pos":self._uiPos, "size":self._uiSize, "text":self._text, "img":self._image, "border":self._border, "actions":self._actions})
		self._uiInterface.stageUIChange(("set_div", self._divID, divOpts))

	def __init__(self, uiInterface:UIInterface, divID, **kwargs):
		self._uiInterface = uiInterface
		self._divID = divID
		self._flags = set(["visible"])
		if "flags" in kwargs:
			self._parent = None
			self.setFlags(kwargs["flags"])
		# _divPositioning member will automatically be used with set_div if parent is a div id, but will be ignored if parent is another GameObject (in which case absolute is used instead)
		self._divPositioning = kwargs.get("divPositioning", "static")
		self._layout = kwargs.get("layout", FreeLayout())
		self._parent = kwargs.get("parent", None)
		self._uiPos = kwargs.get("uiPos", "auto")
		self._uiSize = kwargs.get("uiSize", "auto")
		self._text = kwargs.get("text", None)
		self._image = kwargs.get("image", None)
		self._border = kwargs.get("border", None)
		self._actions = kwargs.get("actions", [])
		self._uiUpdate()

	def getDivID(self):
		return self._divID

	def getFlags(self):
		return self._flags

	def getParent(self):
		return self._parent

	def getUIPos(self):
		return self._uiPos

	def getUISize(self):
		return self._uiSize

	def getText(self):
		return self._text

	def getImage(self):
		return self._image
	
	def getBorder(self):
		return self._border

	def getActions(self):
		return self._actions

	def setFlags(self, *argsFlags, **kwFlags):
		"""
		Each flag must be a string
		Every arg in argsFlags can be either a flag, or an iterable containing flags
		If the iterable is dictionary, a lookup is done for the flag and if it is True it is added, if False it is removed.
		All other iterable types (list, tuple) will only add flags, never remove them.
		kwArgs can be used to add or remove individual flags too by setting the keys to True/False.
		"""
		flagsChanged = False
		argsFlags = list(argsFlags) + [kwFlags]
		for arg in argsFlags:
			if isinstance(arg, str):
				# add flag
				flag = arg
				oldFlag = (flag in self._flags)
				if not oldFlag:
					flagsChanged = True
					self._flags.add(flag)
				continue
			try:
				flags = arg
				for flag in flags:
					assert(isinstance(flag, str))
					oldFlag = (flag in self._flags)
					if isinstance(flags, dict) and not flags[flag]:
						# remove flag
						if oldFlag:
							flagsChanged = True
							self._flags.remove(flag)
					else:
						# add flag
						if not oldFlag:
							self._flags.add(flag)
							flagsChanged = True
			except TypeError:
				raise RuntimeError("setFlags argument must be either a string or iterable: {}".format(arg))
		if self._parent and flagsChanged:
			# TODO: Add optional argument to _uiChange so we can tell it to only update flags
			self._uiUpdate()

	def setParent(self, parent):
		"""parent must be either a string divID or None"""
		if self._parent is parent:
			return
		if not (isinstance(parent, str) or parent == None):
			raise Error("parent of {} must be either string, or None when set directly. parent={}".format(self.divID, str(parent)[:50]))
		if isinstance(self._parent, GameObject):
			self._parent.removeObject(self)
		self._parent = parent
		if "visible" in self._flags:
			self._uiUpdate()

	def setUIPos(self, uiPos):
		if self._uiPos == uiPos:
			return
		self._uiPos = uiPos
		if self._isVisible():
			self._uiInterface.stageUIChange(("set_div", self._divID, {"pos":uiPos}))

	def setUISize(self, uiSize):
		if self._uiSize == uiSize:
			return
		self._uiSize = uiSize
		if self._isVisible():
			self._uiInterface.stageUIChange(("set_div", self._divID, {"size":uiSize}))

	def setText(self, text):
		self._text  = text
		if self._isVisible():
			self._uiInterface.stageUIChange(("set_div", self._divID, {"text":text}))

	def setImage(self, filename):
		self._image = filename
		if self._isVisible():
			self._uiInterface.stageUIChange(("set_div", self._divID, {"img":filename}))

	def setBorder(self, border):
		self._border = border
		if self._isVisible():
			self._uiInterface.stageUIChange(("set_div", self._divID, {"border":border}))

	def setActions(self, actions):
		self._actions = actions
		if self._parent:
			self._uiInterface.stageUIChange(("set_div", self._divID, {"actions":actions}))

	# ------------ children ------------

	def getObject(self, *layoutArgs):
		return self._layout.getObject(*layoutArgs)

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
						object.__uiUpdate()
				else:
					# The parent of object must be a child or descendent, so it should already have been removed by call to self._layout.hasObject
					assert(object._parent is None)
			return True
		return False

	def removeObject(self, object, recursive=False):
		return self.hasObject(object, recursive=recursive, remove=True)


