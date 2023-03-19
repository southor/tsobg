from .UIInterface import UIInterface
from .FreeLayout import FreeLayout


class GameObject():

	def _uiUpdate(self):
		parent = self._parent if self._visible else None
		if isinstance(parent, GameObject):
			divOpts = {"parent":parent.getDivID(), "divPositioning":"absolute"}
		elif isinstance(parent, str):
			divOpts = {"parent":parent, "divPositioning":self._divPositioning}
		elif parent == None:
			divOpts = {"parent":None}
		else:
			raise Error("parent of {} must be either string, GameObject or None. parent={}".format(self.divID, str(parent)[:50]))
		#assert(isinstance(divOpts["parent"], str) or divOpts["parent"] == None)
		if parent != None:
			divOpts.update({"pos":self._uiPos, "size":self._uiSize, "text":self._text, "img":self._image, "border":self._border, "actions":self._actions})
		self._uiInterface.stageUIChange(("set_div", self._divID, divOpts))

	def __init__(self, uiInterface:UIInterface, divID, **kwargs):
		self._uiInterface = uiInterface
		self._divID = divID
		# _divPositioning member will automatically be used with set_div if parent is a div id, but will be ignored if parent is another GameObject (in which case absolute is used instead)
		self._divPositioning = kwargs.get("divPositioning", "static")
		self._layout = kwargs.get("layout", FreeLayout())
		self._parent = kwargs.get("parent", None)
		self._uiPos = kwargs.get("uiPos", "auto")
		self._uiSize = kwargs.get("uiSize", "auto")
		self._visible = kwargs.get("visible", True)
		self._text = kwargs.get("text", None)
		self._image = kwargs.get("image", None)
		self._border = kwargs.get("border", None)
		self._actions = kwargs.get("actions", [])
		self._uiUpdate()

	def getDivID(self):
		return self._divID

	def getParent(self):
		return self._parent

	#def getLayout(self):
	#	return layout

	def getUIPos(self):
		return self._uiPos

	def getUISize(self):
		return self._uiSize

	def getVisible(self):
		return self._visible

	def getText(self):
		return self._text

	def getImage(self):
		return self._image
	
	def getBorder(self):
		return self._border

	def getActions(self):
		return self._actions

	def setParent(self, parent):
		"""parent must be either a string divID or None"""
		if self._parent is parent:
			return
		if not (isinstance(parent, str) or parent == None):
			raise Error("parent of {} must be either string, or None when set directly. parent={}".format(self.divID, str(parent)[:50]))
		if isinstance(self._parent, GameObject):
			self._parent.removeObject(self)
		self._parent = parent
		if self._visible:
			self._uiUpdate()

	def setUIPos(self, uiPos):
		if self._uiPos == uiPos:
			return
		self._uiPos = uiPos
		if self._parent and self._visible:
			self._uiInterface.stageUIChange(("set_div", self._divID, {"pos":uiPos}))

	#def setPos(self, *layoutArgs):
	#	if parent:
	#		parent.layout.setObjectPos(self, *layoutArgs)
	#		return True
	#	else:
	#		return False

	def setUISize(self, uiSize):
		if self._uiSize == uiSize:
			return
		self._uiSize = uiSize
		if self._parent and self._visible:
			self._uiInterface.stageUIChange(("set_div", self._divID, {"size":uiSize}))

	def setVisible(self, visible):
		if self._visible == visible:
			return
		self._visible = visible
		if self._parent:
			self._uiUpdate()	

	def setText(self, text):
		self._text  = text
		if self._parent and self._visible:
			self._uiInterface.stageUIChange(("set_div", self._divID, {"text":text}))

	def setImage(self, filename):
		self._image = filename
		if self._parent and self._visible:
			self._uiInterface.stageUIChange(("set_div", self._divID, {"img":filename}))

	def setBorder(self, border):
		self._border = border
		if self._parent and self._visible:
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
		if object._visible:
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
					if object._visible:
						object.__uiUpdate()
				else:
					# The parent of object must be a child or descendent, so it should already have been removed by call to self._layout.hasObject
					assert(object._parent is None)
			return True
		return False

	def removeObject(self, object, recursive=False):
		return self.hasObject(object, recursive=recursive, remove=True)


		
