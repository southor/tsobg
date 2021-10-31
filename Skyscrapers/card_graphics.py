from PIL import Image, ImageFont, ImageDraw

import os


fonts = {
	"titleFont" : ImageFont.truetype("arial.ttf", 16),
	"textFontL" : ImageFont.truetype("arial.ttf", 14),
	"textFontS" : ImageFont.truetype("arial.ttf", 11)
}

fontHeights = {
	"titleFont" : 16 + 3,
	"textFontL" : 14 + 3,
	"textFontS" : 11 + 3
}


cardOutputFolder = "generated_cards"
cardDebugOutputFolder = "generated_cards_debug"


icons = {}
iconsFolder = "icons"
iconFiles = [f for f in os.listdir(iconsFolder) if os.path.isfile(os.path.join(iconsFolder, f))]
for filename in iconFiles:
	iconName = os.path.splitext(filename)[0]
	icons[iconName] = Image.open(os.path.join(iconsFolder, filename), 'r')

typeColors = {
	"shop" : (200, 0, 0),
	#"service" : (155, 105, 67),
	"office" : (100, 100, 255),
	"apartment" : (0, 150, 0),
	"service" : (200, 0, 255)
}

credibilityNames = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]
credibilityColors = [(56, 94, 15), (110, 139, 61), (150, 185, 72), (255, 193, 37), (255, 134, 0), (224, 64, 6), (128, 42, 42)]


cardWidth = 180
cardHeight = 180
cardBorder = 6

titleSection = (15, 10, 165, 35)
textSection = (15, 40, 165, 145)
costSection = (15, 150, 165, 175)


'''
def gridToPos(gridPos):
	return (gridPos[0] * gridSize, gridPos[1] * gridSize)	
'''

	
def rectTopLeft(rect):
	return (rect[0], rect[1])
	
def rectTopRight(rect):
	return (rect[2], rect[1])

def rectBottomLeft(rect):
	return (rect[0], rect[3])
	
def rectBottomRight(rect):
	return (rect[2], rect[3])

def rectToShape(rect):
	return [(rect[0], rect[1]),
			(rect[2], rect[1]),
			(rect[2], rect[3]),
			(rect[0], rect[3]),
			(rect[0], rect[1])]
	
def parseHexColor(hexColor):
	if len(hexColor) == 0:
		return ()
	else:
		colorValue = int(hexColor[0:2], 16)
		return (colorValue,) + parseHexColor(hexColor[2:])

def colorToHexStr(color):
	return "".join(["{:02x}".format(val) for val in color])

def parseText(text):
	def parseNewlineText(text):
		lines = text.split('\n')
		lastIdx = len(lines) - 1
		pText = []
		for i,line in enumerate(lines):
			if len(line) > 0:
				pText.append(("text", line))
			if i != lastIdx:
				pText.append(("newline", 1))
		return pText
	if len(text) == 0:
		return []
	i = text.find('@') # find command start
	if (i == -1):
		# no command in text
		return parseNewlineText(text)
	# there is a command
	j = i + text[i:].find(';') # find command end
	if j == -1 or '@' in text[i+1:j] != -1:
		# found no ; or found another @ inbetween first @ and next ;
		raise ValueError("command in text not correctly formatted: " + text)
	pText = []
	if i > 0:
		# there is text before command starts
		pText += parseNewlineText(text[0:i])
	cmd = tuple(text[i+1:j].split(':')) # reformat the command
	pText.append(cmd) # add the command
	pText += parseText(text[j+1:]) # recursively parse the rest
	return pText


def calcTextSize(draw, text, fontName):
	font = fonts[fontName]
	fontHeight = fontHeights[fontName]
	x,y = (0,0)
	maxX = 0
	pText = parseText(text)
	rowHeight = fontHeight
	for part in pText:
		w,h = 0,0
		if part[0] == "text":
			#print("text: " + part[1])	
			w,h = draw.textsize(part[1], font=font)
		elif part[0] == "newline":
			#print("newline: ")
			n = float(part[1]) if len(part) >= 1 else 1
			y += round(rowHeight * n)
			x = 0
		elif part[0] == "icon":
			#print("icon: " + part[1])
			name = part[1]
			w,h = icons[name].size
			if rowHeight <  h + 2:
				rowHeight = h + 2
		#print(part[1] + " w: ", w)
		x += w
		if maxX < x:
			maxX = x
	return (maxX, y + rowHeight)
	
def calcStartPos(draw, posInfo, text, fontName):
	xAlign = ""
	yAlign = ""
	i = 0
	while isinstance(posInfo[i], str):
		align = posInfo[i]
		if (not xAlign) and align in ["left", "right"]:
			xAlign = align
		elif (not yAlign) and align in ["top", "bottom"]:
			yAlign = align
		else:
			raise ValueError("incorrect align string: " + posInfo)
		i += 1
	textSize = calcTextSize(draw, text, fontName)
	x = 0
	y = 0
	if len(posInfo) == i+2:
		pos = posInfo[i:]
		if xAlign == "left":
			x = pos[0]
		elif xAlign == "right":
			x = pos[0] - textSize[0]
		else: # center
			x = pos[0] - textSize[0] / 2
		if yAlign == "top":
			y = pos[1]
		elif yAlign == "bottom":
			y = pos[1] - textSize[1]
		else: # center
			y = pos[1] - textSize[1] / 2
	elif len(posInfo) == i+4:
		rect = posInfo[i:]
		if xAlign == "left":
			x = rect[0]
		elif xAlign == "right":
			x = rect[2] - textSize[0]
		else: # center
			x = (rect[0] + rect[2] - textSize[0]) / 2
		if yAlign == "top":
			y = rect[1]
		elif yAlign == "bottom":
			y = rect[3] - textSize[1]
		else: # center
			y = (rect[1] + rect[3] - textSize[1]) / 2
	else:
		raise ValueError("incorrect posInfo: " + posInfo)
	return (int(x),int(y))	
	
	
	
def drawText(img, posInfo, text, fontName):
	draw = ImageDraw.Draw(img)
	font = fonts[fontName]
	fontHeight = fontHeights[fontName]
	x,y = calcStartPos(draw, posInfo, text, fontName)
	startX = x
	prevColors = []
	color = (0,0,0)
	#print("text: " + text)
	pText = parseText(text)
	#print("parts:")
	#for p in pText:
	#	print("   " + str(p))
	rowHeight = fontHeight
	for part in pText:
		w,h = 0,0
		if part[0] == "text":
			#print("text: " + part[1])
			w,h = draw.textsize(part[1], font=font)
			draw.text((x,y), part[1], fill=color+(255,), font=font)
		elif part[0] == "newline":
			#print("newline: ")
			n = float(part[1]) if len(part) >= 1 else 1
			y += round(rowHeight * n)
			# reset values whens tarting a new row
			x = startX
			xRefIdx = 0
			rowHeight = fontHeight
		elif part[0] == "color":
			#print("color: " + part[1])
			if part[1] == "previous":
				if len(prevColors) < 1:
					RuntimeError("Tried to set previous color when stack is empty: ", text)
				color = prevColors.pop()
			else:
				prevColors.append(color)
				color = parseHexColor(part[1])
		elif part[0] == "icon":
			#print("icon: " + part[1])
			name = part[1]
			icon = icons[name]
			w,h = icon.size
			if rowHeight <  h + 2:
				rowHeight = h + 2
			img.paste(icon, (x, y + int((fontHeight-h)/2)))
		elif part[0] == "xref":
			x = startX + int(part[1])
		#print(part[1] + " w: ", w)
		x += w

def resourcesText(rDict):
	resourceList = []
	for entity in rDict:
		resourceStr = str(rDict[entity]) + " @icon:" + entity + ";"
		resourceList.append(resourceStr)
	return "  ".join(resourceList)

def iconList(entities, delimiter):
	if isinstance(entities, str):
		entities = [entities]
	icons = ["@icon:" + e + ";" for e in entities]
	return delimiter.join(icons)
	
def colorTextByType(text, type):
	return "@color:" + colorToHexStr(typeColors[type]) + ";" + text + "@color:previous;"
	
def colorTextByCredibility(text, credibility):
	return "@color:" + colorToHexStr(credibilityColors[credibility]) + ";" + text + "@color:previous;"
	
def floorTypeText(floorTypes, delimiter):
	if isinstance(floorTypes, str):
		floorTypes = [floorTypes]
	# here assume types is a list
	typesWithColors = [colorTextByType(type, type)
							for type in floorTypes]
	return delimiter.join(typesWithColors)

def drawCardBorder(draw, color, w, h, border):
    d = border/2 # draw in center of border
    shape = [(d, d), (w-d, d), (w-d, h-d), (d, h-d), (d, d)]
    draw.line(shape, fill=color, width=0)
	
def drawRect(draw, color, rect):
	draw.line(rectToShape(rect), fill=color, width=0)

def drawSectionBarrier(draw, color, section, sides="all"):
	if sides == "all":
		drawRect(draw, color, section)
	else:
		# define the 4 possible barriers as shapes
		borderShapes = {
			"top": 	  [rectTopLeft(section), 	rectTopRight(section)],
			"bottom": [rectBottomLeft(section), rectBottomRight(section)],
			"left":   [rectTopLeft(section), 	rectBottomLeft(section)],
			"right":  [rectTopRight(section), 	rectBottomRight(section)]
		}
		# convert to list if needed
		if isinstance(sides, str):
			sides = [sides]
		# draw all the requested barriers
		for side in sides:
			draw.line(borderShapes[side], fill=color, width=0)
	
def makeCardFront(title, text, textAlign, fontName, **kwargs):
	picture = kwargs.get("picture", None)
	buyPrice = kwargs.get("buyPrice", None)
	moneyPerTurn = None
	moneyPerTurnTitle = None
	if "hirePrice" in kwargs:
		moneyPerTurn = kwargs["hirePrice"]
		moneyPerTurnTitle = "Hire: "
	if "rent" in kwargs:
		moneyPerTurn = kwargs["rent"]
		moneyPerTurnTitle = "Rent: "
	if "interest" in kwargs:
		moneyPerTurn = kwargs["interest"]
		moneyPerTurnTitle = "Interest: "
	debugSections = kwargs.get("debugSections", False)
	card = Image.new('RGBA', (cardWidth, cardHeight), (255, 255, 255, 255))
	draw = ImageDraw.Draw(card)
	if debugSections:
		for section in [titleSection, textSection, costSection]:
			draw.line(rectToShape(section), fill=(200, 200, 200, 255), width=0)
	drawCardBorder(draw, "grey", cardWidth, cardHeight, cardBorder)
	if picture:
		# TODO: replace by using textSection
		card.paste(picture, (90 - picture.size[0]/2, 90 - picture.size[1]/2))
	if title:
		drawText(card, titleSection, title, "titleFont")
		drawSectionBarrier(draw, "grey", titleSection, "bottom")
	if text:
		drawText(card, textAlign + textSection, text, fontName)
	if moneyPerTurn or buyPrice:
		drawSectionBarrier(draw, "grey", costSection, "top")
	if moneyPerTurn:
		drawText(card, ("left",) + costSection, moneyPerTurnTitle + resourcesText({"money":moneyPerTurn}), "textFontS")
	if buyPrice:
		drawText(card, ("right",) + costSection, "Buy: " + resourcesText({"money":buyPrice}), "textFontS")
	return card

def makeCardBack(imgPath):
	card = Image.new('RGBA', (cardWidth, cardHeight), (255, 255, 255, 255))
	img = Image.open(imgPath, 'r')
	offset = ((cardWidth - img.size[0]) / 2, (cardHeight - img.size[1]) / 2)
	card.paste(img, offset)
	draw = ImageDraw.Draw(card)
	drawCardBorder(draw, "grey", cardWidth, cardHeight, cardBorder)
	return card
		
	
# ----------------------------------------

# buyPrice: the cost in money
# gain: instant gain as dict with type and amount
def makeMaterialCard(buyPrice, gain, **kwargs):
	gainText = resourcesText(gain)
	if buyPrice > 0:
		kwargs["buyPrice"] = buyPrice
	return makeCardFront("Materials", gainText, (), "textFontL", **kwargs)
	
# hirePrice: the hire cost in money
# beauty: a number representing extra building attraction
# types: list of floor type that the architect can create
# maxHeightSteel: max building height the architect can reach for a steel building
# maxHeightConcrete: max building height the architect can reach for a concrete building
def makeArchitectCard(hirePrice, beauty, types, maxHeightSteel, maxHeightConcrete, **kwargs):
	if hirePrice > 0:
		kwargs["hirePrice"] = hirePrice
	text = floorTypeText(types, " / ") + "@newline:1.5;"
	#text = "@color:4444FF;" + ", ".join(types) + "@color:000000;\n"
	text += ("max building height:\n" +
		"    @icon:steel;: " + str(maxHeightSteel) + "\n" +
		"    @icon:concrete;: " + str(maxHeightConcrete) + "@newline:1.5;")
	if beauty > 0:
		text += "+ " + resourcesText({"beauty": beauty}) + "\n"
	return makeCardFront("Architect", text, ("top","left"), "textFontS", **kwargs)

# cost: the hire cost in money
# nFloors: max number of floors it can add to a building
def makeConstructionCard(hirePrice, nFloors, **kwargs):
	nFloorsText = "+ " + resourcesText({"floor":nFloors})
	if hirePrice > 0:
		kwargs["hirePrice"] = hirePrice
	return makeCardFront("Construction Firm", nFloorsText, (), "textFontL", **kwargs)

# tenant ready to move in
def makeTenantCard(name, nFloors, type, rent, criterias = [], **kwargs):
	text = "@newline:0.2;"
	text += colorTextByType(name, type) + "@newline:1.5;"
	text += resourcesText({"floor":nFloors}) + "@newline:1.2;"
	if criterias:
		text += "Criterias:\n"
	for criteria in criterias:
		text += " " + criteria + "\n"
	if rent:
		kwargs["rent"] = rent
	return makeCardFront("Tenant", text, ("top","left"), "textFontS", **kwargs)

# amount: amount of money
# interests: list of interests where each index corresponds to a credibility score
def makeLoanCard(amount, interests, **kwargs):
	text = resourcesText({"money": amount}) + "\n"
	if interests:
		text += "Interest:\n"
		idxRange = range(0, len(credibilityNames))
		for i,interest in enumerate(interests):
			credibilityName = colorTextByCredibility(credibilityNames[i], i)
			text += "    " + credibilityName + "@xref:65;" + str(interest) + "\n"
	return makeCardFront("Loan", text, ("top", "left",), "textFontS", **kwargs)
	
# card for a lot (place on board for sale)
def makeLotCard(district, lotNum, **kwargs):
	text = district + " " + str(lotNum)
	return makeCardFront("Lot for sale", text, ("top",), "textFontL", **kwargs)
	
# buyPrice: the purchase cost in money
# gain: instant gain as dict with type and amount
# production: produces at income phase as dict with type and amount
def makeProductionCard(title, buyPrice, gain, production, **kwargs):
	if buyPrice > 0:
		kwargs["buyPrice"] = buyPrice
	text = ""
	if gain:
		text += resourcesText(gain) + "@newline:1.5;"
	if production:
		text += "Production: " + resourcesText(production)
	return makeCardFront(title, text, ("top",), "textFontL", **kwargs)
	
# buyPrice: the purchase cost in money
# effects: each effect as a string
def makeUpgradeCard(title, buyPrice, *effects, **kwargs):
	if buyPrice > 0:
		kwargs["buyPrice"] = buyPrice
	text = ""
	if effects:
		text += "Effects:\n"
	for effect in effects:
		text += "    " + effect + "\n"
	return makeCardFront(title, text, ("top",), "textFontS", **kwargs)

	
# ----------------------------------------

cardMakeFunctions = {
	"material": makeMaterialCard,
	"architect": makeArchitectCard,
	"construction": makeConstructionCard,
	"tenant": makeTenantCard,
	"loan": makeLoanCard,
	"lot": makeLotCard,
	"production": makeProductionCard,
	"upgrade": makeUpgradeCard
	}

def makeManyCards(category, cardDatas):
	makeCard = cardMakeFunctions[category]
	for i,data in enumerate(cardDatas):
		if isinstance(data, tuple):
			if len(data) == 2:
				nCardCopies = data[0] # for now ignore (needs to be used later to arrange for printing)
				cardArgs = data[1]
			else:
				raise ValueError("Expecting tuple to be of length 2, instead it's " + len(data))
		elif isinstance(data, list):
			nCardCopies = 1
			cardArgs = data
		else:
			raise ValueError("Expecting card data to be either tuple or list, but it's " + type(data))
		filename = cardOutputFolder + "/" + category + "{:02d}.png".format(i+1)
		debugFilename = cardDebugOutputFolder + "/" + category + "{:02d}.png".format(i+1)
		makeCard(*cardArgs).save(filename)
		makeCard(*cardArgs, debugSections=True).save(debugFilename)

def makeMaterialCards():
	makeManyCards("material", [
		(1, [3, {"steel": 3, "concrete": 3}]),
		(1, [3, {"steel": 8}]),
		(1, [4, {"concrete": 10}]),
		(1, [0, {"steel": 2}]),
		(1, [0, {"concrete": 2}]),
		])

def makeArchitectCards():
	# card args: cost, beauty, types, maxHeightSteel, maxHeightConcrete
	makeManyCards("architect", [
		[2, 0, ["shop","service"], 10, 4],
		[2, 0, ["office","apartment"], 10, 5],
		[2, 1, ["apartment","service"], 12, 4],
		[2, 1, ["office"], 10, 5],
		[2, 1, ["shop"], 8, 5]
		])
	
def makeConstructionCards():
	makeManyCards("construction", [
		(1, [4, 6]),
		(1, [3, 4]),
		(1, [2, 2])
		])
		
def makeTenantCards():
	def sumCriteria(termEntities, value):
		return iconList(termEntities, " + ") + " >= " + str(value)
	def buildingsCriteria(n, types, location):
		return str(n) + " " + floorTypeText(types, "/") + " buildings " + "@icon:" + location + ";"
	def tenantsCriteria(n, type):
		return str(n) + " " + colorTextByType(type, type) + " tenants " + "@icon:location_same_building;"
	def nextToCriteria(n, tileType, location):
		return str(n) + " " + iconList([tileType, location], " ")
	tenants = [
		["Catz Mobile Games", 4, "office", 8, [sumCriteria(["beauty","free_view"], 4), buildingsCriteria(3, "office", "location_nearby")]],
		["No Fluke Insurances ", 2, "office", 4, [buildingsCriteria(3, "office", "location_nearby")]],
		["\"Grounded\" Music Studio ", 1, "office", 2, []],
		["Dedication Apartment Gym ", 1, "service", 3, [tenantsCriteria(3, "apartment")]],
		["Doctors Office ", 1, "service", 4, ["below floor 5", buildingsCriteria(5, ["office", "apartment"], "location_nearby")]],
		["Bernie Burgers ", 1, "service", 3, ["below floor 3", buildingsCriteria(3, ["office", "apartment"], "location_nearby")]],
		["Corner Groceries ", 1, "shop", 2, ["bottom floor", buildingsCriteria(3, "apartment", "location_next_to_including")]],
		["Olsen Department Store ", 2, "shop", 3, ["below floor 4", nextToCriteria(1, "parking", "location_next_to")]],
		["Great View Hotel ", 2, "service", 5, ["above floor 7", sumCriteria("free_view", 4)]]
	]
	makeManyCards("tenant", tenants)
	
def makeLoanCards():
	makeManyCards("loan", [
		(1, [10, [0, 1, 1, 2, 3, 5, 7]]),
		(1, [10, [0, 0, 1, 2, 2, 4, 6]]),
		(1, [8, [0, 1, 1, 2, 3, 4, 7]]),
		(1, [8, [0, 0, 1, 2, 2, 4, 7]])
		])

def makeLotCards():
	# 6 districts? A-F
	# 9 tiles per district?
	makeManyCards("lot", [
		["A", 1],
		["B", 3]
		])
	
def makeProductionCards():
	makeManyCards("production", [
		["steel mill", 9, {"steel": 2}, {"steel": 2}],
		["concrete factory", 8, {}, {"concrete": 4}]
		])
	
def makeUpgradeCards():
	makeManyCards("upgrade", [
		["Material Engineer", 3,
			"-1 @icon:steel; when building >= 3 floors",
			"-2 @icon:steel; when building >= 3 floors"],
		["Material Engineer", 3,
				"-1 @icon:steel; when building >= 4 floors",
				"-2 @icon:steel; when building >= 6 floors"],
		["Strength Engineer", 4, "+2 max building height"],
		["Strength Engineer", 6, "+4 max building height"],
		["Talented Broker", 6, "Ignore one criteria when taking a tenant"]
			])
	
if __name__ == "__main__":
	makeMaterialCards()
	makeArchitectCards()
	makeConstructionCards()
	makeTenantCards()
	makeLoanCards()
	makeLotCards()
	makeProductionCards()
	makeUpgradeCards()
	
	