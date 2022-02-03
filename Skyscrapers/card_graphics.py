# Run this file to generate cards
# It creates three card folders, one for online game, one for printing, and one for graphics debugging

from PIL import Image, ImageFont, ImageDraw
import os
from pathlib import Path

pathHere = Path(__file__).absolute().parent

import card_data
import graphics


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

cardOutputFolder = pathHere / "generated_cards"
cardDebugOutputFolder = pathHere / "generated_cards_debug"
cardOnlineOutputFolder = pathHere / "generated_cards_online"

cardWidth = 180
cardHeight = 180
cardBorder = 6

titleSection = (15, 10, 165, 35)
textSection = (15, 40, 165, 145)
costSection = (15, 150, 165, 175)

cardSize = (cardWidth, cardHeight)

cardColor = (255, 255, 255, 255)
raiseColor = (180, 180, 180, 255)

icons = graphics.getIconImages()

typeColors = {
	"shop" : (200, 0, 0),
	#"service" : (155, 105, 67),
	"office" : (100, 100, 255),
	"apartment" : (0, 150, 0),
	"service" : (200, 0, 255)
}

credibilityNames = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]
credibilityColors = [(56, 94, 15), (110, 139, 61), (150, 185, 72), (255, 193, 37), (255, 134, 0), (224, 64, 6), (128, 42, 42)]


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
	
def parseHexColor(hexColor):
	if len(hexColor) == 0:
		return ()
	else:
		colorValue = int(hexColor[0:2], 16)
		return (colorValue,) + parseHexColor(hexColor[2:])

def colorToHexStr(color):
	return "".join(["{:02x}".format(val) for val in color])
	
# can only deal with positive numbers
def writtenNumber(n: int):
	if n < 0:
		raise ValueError("Number < 0: " + str(n))
	if n == 0:
		return "zero"
	elif n == 1:
		return "one"
	elif n == 2:
		return "two"
	elif n == 3:
		return "three"
	else:
		return str(n)

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
					raise RuntimeError("Tried to set previous color when stack is empty: ", text)
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
	
def colorTextByType(text, type):
	return "@color:" + colorToHexStr(typeColors[type]) + ";" + text + "@color:previous;"
	
def colorTextByCredibility(text, credibility):
	return "@color:" + colorToHexStr(credibilityColors[credibility]) + ";" + text + "@color:previous;"

def iconList(entities, delimiter):
	if isinstance(entities, str):
		entities = [entities]
	icons = ["@icon:" + e + ";" for e in entities]
	return delimiter.join(icons)

def floorTypeText(floorTypes, delimiter):
	if isinstance(floorTypes, str):
		floorTypes = [floorTypes]
	# here assume types is a list
	typesWithColors = [colorTextByType(type, type)
							for type in floorTypes]
	return delimiter.join(typesWithColors)
	
def tenantCriteriaText(tenantCriteria):
	textLambdas = {
		"aboveFloor" : lambda floorN: "above floor " + str(floorN),
		"belowFloor" : lambda floorN: "below floor " + str(floorN),
		"groundFloor" : lambda : "ground floor",
		"proximityBuildings" : lambda n,types,location: str(n) + " " + floorTypeText(types, "/") + " buildings " + "@icon:" + location + ";",
		"proximityLots" : lambda n,lotType,location: str(n) + " " + iconList([lotType, location], " "),
		"nTenants" : lambda n,type: str(n) + " " + colorTextByType(type, type) + " tenants " + "@icon:location_same_building;",
		"entitySum>=" : lambda termEntities,value: iconList(termEntities, " + ") + " >= " + str(value)
	}
	criteriaType,criteriaArgs = card_data.unpackCriteria(tenantCriteria)
	return textLambdas[criteriaType](*criteriaArgs)
	
def upgradeEffectText(effect):
	def discountText(material, nFloorsCondition, discountAmount):
		return str(discountAmount) + " @icon:" + material + "; when building >= " + str(nFloorsCondition) + " floors"
	def discountTextMulti(material, floorsDiscounts):
		discountTextLines = ["  " + discountText(material, nFloorsCondition, discountAmount) for nFloorsCondition,discountAmount in floorsDiscounts]
		return "material discount:\n" + "\n".join(discountTextLines)
	textLambdas = {
		"materialDiscount" : discountTextMulti,
		"increaseMaxHeight" : lambda nFloors: "+" + str(nFloors) + " max building height",
		"ignoreTenantCriteria" : lambda n: "Ignore " + writtenNumber(n) + " criteria when\npicking a tenant",
		"cardDiscount" : lambda n: "card discound:\n " + str(n) + " @icon:money; for every hire/buy cost",
		"takeCards" : lambda n: "Take extra cards:\n" + "Discard this card to take up to\n" + str(n) + " cards instead of one during\ncard phase."
	}
	effectType,effectArgs = card_data.unpackEffect(effect)
	return textLambdas[effectType](*effectArgs)

def drawBorder(draw, color, w, h, border):
	d = border/2 # draw in center of border
	shape = [(d, d), (w-d-1, d), (w-d-1, h-d-1), (d, h-d-1), (d, d)]
	draw.line(shape, fill=color, width=0)
	
def drawRaise(draw, x, y, w, h, **kwargs):
	color = kwargs.get("color", raiseColor)
	if "fill" in kwargs:
		fillColor = kwargs["fill"]
		draw.rectangle([x, y, x+w, y+h], fill=fillColor)
	shape = [(x, y), (x, y+h-1), (x+w-1, y+h-1)]
	draw.line(shape, fill=color, width=1)

def drawSectionBarrier(draw, color, section, sides="all"):
	if sides == "all":
		#drawRect(draw, color, section)
		draw.rectangle(section, outline=color, width=1)
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
	
def makeTextCard(title, text, textAlign, fontName, **kwargs):
	doDrawRaise = kwargs.get("drawRaise", False)
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
	card = Image.new('RGBA', (cardWidth, cardHeight), cardColor)
	draw = ImageDraw.Draw(card)
	if debugSections:
		for section in [titleSection, textSection, costSection]:
			#draw.line(rectToShape(section), fill=(200, 200, 200, 255), width=0)
			draw.rectangle(section, outline=(200, 200, 200, 255), width=1)
	drawBorder(draw, "grey", cardWidth, cardHeight, cardBorder)
	if doDrawRaise:
		drawRaise(draw, 0, 0, cardWidth, cardHeight)
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

def makeImageCard(imgPath, **kwargs):
	doDrawRaise = kwargs.get("drawRaise", False)
	card = Image.new('RGBA', (cardWidth, cardHeight), (255, 255, 255, 255))
	img = Image.open(imgPath, 'r')
	offsetX = (cardWidth - img.size[0]) / 2
	offsetY = (cardHeight - img.size[1]) / 2
	offset = (int(offsetX), int(offsetY))
	card.paste(img, offset)
	draw = ImageDraw.Draw(card)
	drawBorder(draw, "grey", cardWidth, cardHeight, cardBorder)
	if doDrawRaise:
		drawRaise(draw, 0, 0, cardWidth, cardHeight)
	return card
	
def makeDeckImage(topCardImg, nOutlines):
	spacing = 2
	outlineColor = (160, 160, 160, 255)
	expand = nOutlines * spacing # init enough space in the image
	img = Image.new('RGBA', (cardWidth + expand, cardHeight + expand), (255, 255, 255, 0))
	draw = ImageDraw.Draw(img)
	offsetX = 0
	offsetY = expand
	for i in range(0, nOutlines):
		drawRaise(draw, offsetX, offsetY, cardWidth, cardHeight, fill=cardColor)
		offsetX += spacing
		offsetY -= spacing
	img.paste(topCardImg, (offsetX, offsetY))
	return img
	
# ----------------------------------------

# buyPrice: the cost in money
# gain: instant gain as dict with type and amount
def makeMaterialsCard(**kwargs):
	type = kwargs.pop("type")
	gainText = resourcesText(kwargs.pop("gain"))
	if type == "supply":
		return makeTextCard("Materials supply", gainText, (), "textFontL", **kwargs)
	elif type == "contract":
		extraText = "\n\nDiscard this card to use the\nmaterials in a single\nconstruction project"
		return makeTextCard("Materials contract", gainText + extraText, ("top",), "textFontS", **kwargs)
	else:
		raise RuntimeError("Unknown Materials card type: " + type)

# hirePrice: the hire cost in money
# beauty: a number representing extra building attraction
# types: list of floor type that the architect can create
# maxHeightSteel: max building height the architect can reach for a steel building
# maxHeightConcrete: max building height the architect can reach for a concrete building
def makeArchitectCard(**kwargs):
	beauty = kwargs.pop("beauty", 0)
	types = kwargs.pop("types")
	maxHeightSteel = kwargs.pop("maxHeightSteel", 0)
	maxHeightConcrete = kwargs.pop("maxHeightConcrete", 0)
	text = floorTypeText(types, " / ") + "@newline:1.5;"
	#text = "@color:4444FF;" + ", ".join(types) + "@color:000000;\n"
	text += ("max building height:\n" +
		"    @icon:steel;: " + str(maxHeightSteel) + "\n" +
		"    @icon:concrete;: " + str(maxHeightConcrete) + "@newline:1.5;")
	if beauty > 0:
		text += "+ " + resourcesText({"beauty": beauty}) + "\n"
	return makeTextCard("Architect", text, ("top","left"), "textFontS", **kwargs)

# cost: the hire cost in money
# nFloors: max number of floors it can add to a building
def makeConstructionCard(**kwargs):
	nFloors = kwargs.pop("nFloors")
	nFloorsText = "+ " + resourcesText({"floor":nFloors})
	return makeTextCard("Construction Firm", nFloorsText, (), "textFontL", **kwargs)

# tenant ready to move in
def makeTenantCard(**kwargs):
	name = kwargs.pop("name")
	nFloors = kwargs.pop("nFloors")
	type = kwargs.pop("type")
	criterias = kwargs.pop("criterias", [])
	text = "@newline:0.2;"
	text += colorTextByType(name, type) + "@newline:1.5;"
	text += resourcesText({"floor":nFloors}) + "@newline:1.2;"
	if criterias:
		text += "Criterias:\n"
	for criteria in criterias:
		#text += " " + criteria + "\n"
		text += " " + tenantCriteriaText(criteria) + "\n"
	return makeTextCard("Tenant", text, ("top","left"), "textFontS", **kwargs)

# amount: amount of money
# interests: list of interests where each index corresponds to a credibility score
def makeLoanCard(**kwargs):
	amount = kwargs.pop("amount")
	interests = kwargs.pop("interests")
	text = resourcesText({"money": amount}) + "\n"
	if interests:
		text += "Interest:\n"
		idxRange = range(0, len(credibilityNames))
		for i,interest in enumerate(interests):
			credibilityName = colorTextByCredibility(credibilityNames[i], i)
			text += "    " + credibilityName + "@xref:65;" + str(interest) + "\n"
	return makeTextCard("Loan", text, ("top", "left",), "textFontS", **kwargs)
	
# card for a lot (place on board for sale)
def makeLotCard(**kwargs):
	district = kwargs.pop("district")
	lotNum = kwargs.pop("lotNum")
	text = district + " " + str(lotNum)
	return makeTextCard("Lot for sale", text, ("top",), "textFontL", **kwargs)
	
# buyPrice: the purchase cost in money
# gain: instant gain as dict with type and amount
# production: produces at income phase as dict with type and amount
def makeProductionCard(**kwargs):
	title = kwargs.pop("title")
	gain = kwargs.pop("gain", {})
	production = kwargs.pop("production", {})
	text = ""
	if gain:
		text += resourcesText(gain) + "@newline:1.5;"
	if production:
		text += "Production: " + resourcesText(production)
	return makeTextCard(title, text, ("top",), "textFontL", **kwargs)
	
# buyPrice: the purchase cost in money
# effects: each effect as a string
def makeUpgradeCard(**kwargs):
	title = kwargs.pop("title")
	effects = kwargs.pop("effects", [])
	text = ""
	for effect in effects:
		# TODO, italic style?
		text += upgradeEffectText(effect) + "\n"
	return makeTextCard(title, text, ("top",), "textFontS", **kwargs)

def makeCardBack(**kwargs):
	graphicsFilePath = graphics.getGrapchisFilepath("cardBackIllustration.png")
	return makeImageCard(graphicsFilePath, **kwargs)
	
# ----------------------------------------

cardMakeFunctions = {
	"materials": makeMaterialsCard,
	"architect": makeArchitectCard,
	"construction": makeConstructionCard,
	"tenant": makeTenantCard,
	"loan": makeLoanCard,
	"lot": makeLotCard,
	"production": makeProductionCard,
	"upgrade": makeUpgradeCard
	}
	
def makeAndSaveDeck(name, topCard, nDeckImages):
	for nOutlines in range(1, nDeckImages+1):
		deck = makeDeckImage(topCard, nOutlines)
		name = name + "_deck" + "{:02d}.png".format(nOutlines)
		deck.save(str(cardOnlineOutputFolder / name))
	
def makeAndSaveCard(makeCardFunc, name, cardKWArgs = {}, **kwargs):
	nDeckImages = kwargs.get("nDeckImages", 0)
	filename = name + ".png"
	filePath = cardOutputFolder / filename
	debugFilePath = cardDebugOutputFolder / filename
	onlineFilePath = cardOnlineOutputFolder / filename
	makeCardFunc(**cardKWArgs).save(str(filePath))
	makeCardFunc(**cardKWArgs, debugSections=True).save(str(debugFilePath))
	cardOnline = makeCardFunc(**cardKWArgs, drawRaise=True)
	cardOnline.save(str(onlineFilePath))
	if nDeckImages > 0:
		makeAndSaveDeck(name, cardOnline, nDeckImages)
	
def makeAndSaveCards(cardDatas):
	for cardData in cardDatas:
		category = cardData["category"]
		makeAndSaveCard(cardMakeFunctions[category], cardData["name"], cardData["cardKWArgs"])

def makeAllCardImages():
	cardOutputFolder.mkdir(exist_ok=True)
	cardDebugOutputFolder.mkdir(exist_ok=True)
	cardOnlineOutputFolder.mkdir(exist_ok=True)
	cardDatas = card_data.cardDatas
	makeAndSaveCards(cardDatas) # card fronts
	makeAndSaveCard(makeCardBack, "cardBack", nDeckImages=6) # card back (with deck images)

if __name__ == "__main__":
	print("generating cards...")
	makeAllCardImages()
	print("done")
	
	