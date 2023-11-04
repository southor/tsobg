from pathlib import Path
import sys

pathHere = Path(__file__).absolute().parent

# tsobg imports
sys.path.append(str(pathHere.parent.parent))
from tsobg import UIGrid
from tsobg import UIInterface
from tsobg import ActionReceiver

# import SkyScraper cards
from Card import Card
from CardGrid import CardGrid

class PlayerArea(CardGrid):
	
	def _getPlayerSupplyItemDivID(self, itemName, elementType):
		return "player_" + itemName + "_" + elementType + "_" + str(self.seatN)

	itemsYOffset = 50
	itemsYInterval = 30

	def __init__(self, uiInterface: UIInterface, actionReceiver:ActionReceiver, seatN, surfaceDivID, items):
		super().__init__(uiInterface, surfaceDivID, (2, 1), uiOffsetPos=(50,0), maxNCards=100)
		self.actionReceiver = actionReceiver
		self.seatN = seatN
		#self.surfaceDivId = surfaceDivId
		# init player supply items divs
		for i,itemName in enumerate(["money", "steel", "concrete"]):
			yPos = PlayerArea.itemsYOffset + i * PlayerArea.itemsYInterval
			# set img div
			divID = self._getPlayerSupplyItemDivID(itemName, "img")
			imgPath = "game_file/icons/" + itemName + ".png"
			divOpts = {"divPositioning":"absolute", "parent":surfaceDivID, "img":imgPath, "pos":(10, yPos)}
			uiInterface.stageUIChange(("set_div", divID, divOpts))
			# set text div
			divID = self._getPlayerSupplyItemDivID(itemName, "text")
			text = str(items.get(itemName, 0))
			divOpts = {"divPositioning":"absolute", "parent":surfaceDivID, "text":text, "pos":(30, yPos), "size":("auto", 16)}
			uiInterface.stageUIChange(("set_div", divID, divOpts))

	def setItemAmount(self, itemName, amount):
		textDivID = self._getPlayerSupplyItemDivID(itemName, "text")
		self.uiInterface.stageUIChange(("set_div", textDivID, {"text":str(amount)}))

	def addCard(self, card:Card):
		#return super().addCard(card, {"selectable":True})
		return super().addCard(card)

	def removeCard(self, card:Card):
		return super().removeCard(card)

