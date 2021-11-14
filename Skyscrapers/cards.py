import random

# TODO: rename to card_datas.py and create also card_logics.py ?

# TODO: tenantCriteria should be a class?

# Each cardData is [category: string, nCardCopies: int, kwargs: dict]
# card id is equal to the index in this list
cardDatas = []

# returns category,nCardCopies,kwargs
def unpackCardData(cardData: tuple):
	return cardData

# returns criteriaType,criteriaArgs
def unpackCriteria(criteria: tuple):
	return (criteria[0], criteria[1:])
	
# returns effectType,effectArgs
def unpackEffect(effect: tuple):
	return (effect[0], effect[1:])

	
	
# convert from (category, header, rows) to (category, nCardCopies, kwargs)
# where header strigns are used as key when filling kwargs
def addCardDatas(category, header, rows):
	try:
		nCopiesIdx = header.index("nCardCopies")
	except ValueError:
		nCopiesIdx = None
	for row in rows:
		#cardData = [category, 1, {}]
		nCopies = 1
		kwargs = {}
		for i,x in enumerate(row):
			if i == nCopiesIdx:
				nCopies = x
			else:
				key = header[i]
				kwargs[key] = x
		cardDatas.append((category, nCopies, kwargs))

addCardDatas("material",
	("nCardCopies", "buyPrice", "gain"), [
		(1, 3, {"steel": 3, "concrete": 3}),
		(1, 3, {"steel": 8}),
		(1, 4, {"concrete": 10}),
		(1, 0, {"steel": 2}),
		(1, 0, {"concrete": 2})
	])

addCardDatas("architect",	
	("hirePrice", "beauty", "types", "maxHeightSteel", "maxHeightConcrete"), [
		(2, 0, ["shop","service"], 10, 4),
		(2, 0, ["office","apartment"], 10, 5),
		(2, 1, ["apartment","service"], 12, 4),
		(2, 1, ["office"], 10, 5),
		(2, 1, ["shop"], 8, 5)
		])
		
addCardDatas("construction",
	("nCardCopies", "hirePrice", "nFloors"), [
		(1, 4, 6),
		(1, 3, 4),
		(1, 2, 2)
		])

def tenantCardDatas():
	return ("tenant", ("name", "nFloors", "type", "rent", "criterias"), [
				("Catz Mobile Games", 4, "office", 8, [("entitySum>=", ["beauty","free_view"], 4), ("proximityBuildings", 3, "office", "location_nearby")]),
				("No Fluke Insurances ", 2, "office", 4, [("proximityBuildings", 3, "office", "location_nearby")]),
				("\"Grounded\" Music Studio ", 1, "office", 2, [("groundFloor",)]),
				("Dedication Apartment Gym ", 1, "service", 3, [("nTenants", 3, "apartment")]),
				("Doctors Office ", 1, "service", 4, [("belowFloor", 5), ("proximityBuildings", 5, ["office", "apartment"], "location_nearby")]),
				("Bernie Burgers ", 1, "service", 3, [("belowFloor", 3), ("proximityBuildings", 3, ["office", "apartment"], "location_nearby")]),
				("Corner Groceries ", 1, "shop", 2, [("groundFloor",), ("proximityBuildings", 3, "apartment", "location_next_to_including")]),
				("Olsen Department Store ", 2, "shop", 3, [("belowFloor", 4), ("proximityLots", 1, "parking", "location_next_to")]),
				("Great View Hotel ", 2, "service", 5, [("aboveFloor", 7), ("entitySum>=", ["free_view"], 4)])
			])

addCardDatas(*tenantCardDatas())


addCardDatas("loan",
	("nCardCopies", "amount", "interests"), [
		(1, 10, [0, 1, 1, 2, 3, 5, 7]),
		(1, 10, [0, 0, 1, 2, 2, 4, 6]),
		(1, 8,  [0, 1, 1, 2, 3, 4, 7]),
		(1, 8,  [0, 0, 1, 2, 2, 4, 7])
		])

addCardDatas("lot",
	("district", "lotNum"), [
		("A", 1),
		("B", 3)
		])

addCardDatas("production",
	("title", "buyPrice", "gain", "production"), [
		("steel mill", 9, {"steel": 2}, {"steel": 2}),
		("concrete factory", 8, {}, {"concrete": 4})
		])

addCardDatas("upgrade",	
	("title", "buyPrice", "effects"), [
		("Material Engineer", 3, [("materialDiscount", "steel", [(3, -1), (5, -2)])]), 
		("Material Engineer", 3, [("materialDiscount", "steel", [(4, -1), (6, -2)])]),
		("Strength Engineer", 4, [("increaseMaxHeight", 2)]),
		("Strength Engineer", 6, [("increaseMaxHeight", 4)]),
		("Talented Broker", 6, [("ignoreTenantCriteria", 1)])
		])	
	
def makeDeck():
	deck = []
	for i,cardData in enumerate(cardDatas):
		category,nCardCopies,kwargs = unpackCardData(cardData)
		deck += [i] * nCardCopies
	random.shuffle(deck)
	return deck
		