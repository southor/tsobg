from pathlib import Path
import sys

pathHere = Path(__file__).absolute().parent

# tsobg imports
sys.path.append(str(pathHere.parent.parent))
from tsobg import UIGrid
from tsobg import UIChangeInterface


class PlayerArea(object):
	
	def __getPlayerSupplyItemDivID(self, itemName, elementType):
		return "player_" + itemName + "_" + elementType + "_" + str(self.seatN)

	itemsYOffset = 50
	itemsYInterval = 30

	def __init__(self, uiInterface: UIChangeInterface, seatN, surfaceDivId, items):
		self.uiInterface = uiInterface
		self.seatN = seatN
		self.surfaceDivId = surfaceDivId
		for i,itemName in enumerate(["money", "steel", "concrete"]):
			yPos = PlayerArea.itemsYOffset + i * PlayerArea.itemsYInterval
			# set img div
			divID = self.__getPlayerSupplyItemDivID(itemName, "img")
			imgPath = "game_file/icons/" + itemName + ".png"
			divOpts = {"parent":surfaceDivId, "img":imgPath, "pos":(10, yPos)}
			uiInterface.stageUIChange_AllPlayers(("set_div", divID, divOpts))
			# set text div
			divID = self.__getPlayerSupplyItemDivID(itemName, "text")
			text = str(items.get(itemName, 0))
			divOpts = {"parent":surfaceDivId, "text":text, "pos":(30, yPos), "size":("auto", 16)}
			uiInterface.stageUIChange_AllPlayers(("set_div", divID, divOpts))

	def setItemAmount(self, itemName, amount):
		textDivID = self.__getPlayerSupplyItemDivID(itemName, "text")
		self.uiInterface.stageUIChange_AllPlayers(("set_div", textDivID, {"text":str(amount)}))

		


