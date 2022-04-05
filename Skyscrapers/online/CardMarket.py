import sys
from pathlib import Path

# tsobg imports
pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent.parent))
from tsobg import Deck
from tsobg import UIInterface

# import SkyScraper cards
from Card import Card, createAllCards
from CardGrid import CardGrid


class CardMarket(CardGrid):
	
	def __initCardDict(self, allCards):
		self.cardDict = {}
		for card in allCards:
			self.cardDict[card.id] = card
	
	def __lookupCardId(self, cardId):
		return self.cardDict[cardId]
	
	def __init__(self, uiInterface:UIInterface):
		super().__init__(uiInterface, "card_market", (5, 3))
		uiInterface.stageUIChange(("set_div", "card_market", {"parent": "center"}))
		allCards = createAllCards()
		self.__initCardDict(allCards)
		self.deck = Deck(allCards)
	
	def fillUp(self):
		nMissingCards = self.getNSpaces() - self.nCards()
		newCards = self.deck.draw(nMissingCards)
		for card in newCards:
			self.addCard(card, {"actions":[("take_card", card.id)]})

	def removeCard(self, cardId):
		card = self.__lookupCardId(cardId)
		return super().removeCard(card, {"actions":[]})
	
	