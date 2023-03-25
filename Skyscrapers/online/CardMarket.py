import sys
from pathlib import Path

# tsobg imports
pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent.parent))
from tsobg import Deck
from tsobg import UIInterface
from tsobg import ActionReceiver

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
	
	def __init__(self, uiInterface:UIInterface, actionReveiver:ActionReceiver):
		super().__init__(uiInterface, "card_market", (5, 3))
		uiInterface.stageUIChange(("set_div", "card_market", {"parent": "center"}))
		allCards = createAllCards()
		self.__initCardDict(allCards)
		self.deck = Deck(allCards)
		self.actionReveiver = actionReveiver
	
	def fillUp(self):
		nMissingCards = self.getNSpaces() - self.nCards()
		newCards = self.deck.draw(nMissingCards)
		for card in newCards:
			imgActions = [(self.actionReveiver, "take_card", card.id, "ia")]
			self.addCard(card, {"imgActions":imgActions})

	def removeCard(self, cardId) -> Card:
		""" If card exists it is removed and returned. otherwise None is returned. """
		card = self.__lookupCardId(cardId)
		if super().removeCard(card, {"actions":[]}):
			return card
		else:
			return None
	
	