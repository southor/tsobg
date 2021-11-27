import sys
from pathlib import Path

pathHere = Path(__file__).absolute().parent

# import tsobg UIChangeInterface
sys.path.append(str(pathHere.parent.parent))
from tsobg import UIChangeInterface

# import SkyScraper card_data
sys.path.append(str(pathHere.parent))
import card_data

def createAllCards():
	res = []
	for cardData in card_data.cardDatas:
		for i in range(0, cardData["nDuplicates"]):
			res.append(Card(cardData, i))
	return res

class Card():

	def __init__(self, cardData, duplicateN):
		self.data = cardData
		self.id = cardData["name"] + "_d" + str(duplicateN)
		self.divCreated = False
		
	def __getFilename(self):
		return "game_file/generated_cards_online/" + self.data["name"] + ".png"

	def __newDivData(self):
		if self.divCreated:
			return {}
		else:
			self.divCreated = True
			return {"img":self.__getFilename()}
		
	def sameCardAs(self, otherCard):
		return self.data is otherCard.data
		
	def setDiv(self, uiInterface: UIChangeInterface, **kwArgs):
		divData = self.__newDivData()
		divData.update(kwArgs)
		uiInterface.addUIChange(("set_div", self.id, divData))