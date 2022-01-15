import sys
from pathlib import Path

pathHere = Path(__file__).absolute().parent

# import tsobg UIInterface
sys.path.append(str(pathHere.parent.parent))
from tsobg import UIInterface

# import SkyScraper card_data
sys.path.append(str(pathHere.parent))
import card_data

cardsFolder = "generated_cards_online"


def checkCardImageFiles():
	cardsFolderPath = pathHere.parent / cardsFolder
	if cardsFolderPath.exists() and cardsFolderPath.is_dir():
		return ""
	else:
		return "\nCard image files not generated! Please run card_graphics.py and restart server\n"

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
		return "game_file/" + cardsFolder + "/" + self.data["name"] + ".png"

	def __newDivOpts(self):
		if self.divCreated:
			return {}
		else:
			self.divCreated = True
			return {"img":self.__getFilename()}
		
	def sameCardAs(self, otherCard):
		return self.data is otherCard.data
		
	def setDiv(self, uiInterface: UIInterface, **divOpts):
		""" stages set_div on uiInterface for this card with divOpts, img is added automatically to divOpts """
		divOpts2 = self.__newDivOpts()
		divOpts2.update(divOpts)
		uiInterface.stageUIChange_AllPlayers(("set_div", self.id, divOpts2))