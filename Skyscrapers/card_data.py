
# TODO: tenantCriteria should be a class?

# Each cardData is a dict with category, nDuplicates, cardKWArgs
cardDatas = []

# returns criteriaType,criteriaArgs
def unpackCriteria(criteria: tuple):
	return (criteria[0], criteria[1:])
	
# returns effectType,effectArgs
def unpackEffect(effect: tuple):
	return (effect[0], effect[1:])

__categoryCounters = {} # contains cumber of each category
	
def __generateCardName(category):
	def getPostfixNum(category):
		if category in __categoryCounters:
			__categoryCounters[category] += 1
		else:
			__categoryCounters[category] = 1
		return __categoryCounters[category]
	n = getPostfixNum(category)
	return "card_" + category + "{:02d}".format(n)

# convert from (category, header, rows) to (category, nDuplicates, kwargs)
# where header strigns are used as key when filling kwargs
def __addCardDatas(category, header, rows):
	try:
		nDuplicatesIdx = header.index("nDuplicates")
	except ValueError:
		nDuplicatesIdx = None
	for row in rows:
		name = __generateCardName(category)
		nDuplicates = 1
		kwargs = {}
		for i,x in enumerate(row):
			if i == nDuplicatesIdx:
				nDuplicates = x
			else:
				key = header[i]
				kwargs[key] = x
		cardData = {"category":category, "name":name, "nDuplicates":nDuplicates, "cardKWArgs":kwargs}
		cardDatas.append(cardData)

__addCardDatas("material",
	("nDuplicates", "buyPrice", "gain"), [
		(1, 3, {"steel": 3, "concrete": 3}),
		(1, 3, {"steel": 8}),
		(1, 4, {"concrete": 10}),
		(1, 0, {"steel": 2}),
		(1, 0, {"concrete": 2})
	])

__addCardDatas("architect",	
	("hirePrice", "beauty", "types", "maxHeightSteel", "maxHeightConcrete"), [
		(2, 0, ["shop","service"], 10, 4),
		(2, 0, ["office","apartment"], 10, 5),
		(2, 1, ["apartment","service"], 12, 4),
		(2, 1, ["office"], 10, 5),
		(2, 1, ["shop"], 8, 5)
		])
		
__addCardDatas("construction",
	("nDuplicates", "hirePrice", "nFloors"), [
		(1, 4, 6),
		(1, 3, 4),
		(1, 2, 2)
		])

def __tenantCardDatas():
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

__addCardDatas(*__tenantCardDatas())


__addCardDatas("loan",
	("nDuplicates", "amount", "interests"), [
		(1, 10, [0, 1, 1, 2, 3, 5, 7]),
		(1, 10, [0, 0, 1, 2, 2, 4, 6]),
		(1, 8,  [0, 1, 1, 2, 3, 4, 7]),
		(1, 8,  [0, 0, 1, 2, 2, 4, 7])
		])

__addCardDatas("lot",
	("district", "lotNum"), [
		("A", 1),
		("B", 3)
		])

__addCardDatas("production",
	("title", "buyPrice", "gain", "production"), [
		("steel mill", 9, {"steel": 2}, {"steel": 2}),
		("concrete factory", 8, {}, {"concrete": 4})
		])
		
# add wearhouse card (stores materials) ?
# add material trader card (sell material at any time) ?
		
__addCardDatas("upgrade",	
	("title", "buyPrice", "effects"), [
		("Material Engineer", 3, [("materialDiscount", "steel", [(3, -1), (5, -2)])]), 
		("Material Engineer", 3, [("materialDiscount", "steel", [(4, -1), (6, -2)])]),
		("Strength Engineer", 4, [("increaseMaxHeight", 2)]),
		("Strength Engineer", 6, [("increaseMaxHeight", 4)]),
		("Talented Broker", 6, [("ignoreTenantCriteria", 1)])
		])
		