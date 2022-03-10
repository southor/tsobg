from PIL import Image
from pathlib import Path

pathHere = Path(__file__).absolute().parent

iconsFolder = pathHere / "icons"
graphicsFolder = pathHere / "graphics"

graphicsOutputFolder = pathHere / "generated_graphics"

raiseColor = (180, 180, 180, 255)


def rectTopLeft(rect):
	return (rect[0], rect[1])
	
def rectTopRight(rect):
	return (rect[2], rect[1])

def rectBottomLeft(rect):
	return (rect[0], rect[3])
	
def rectBottomRight(rect):
	return (rect[2], rect[3])

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



#def getIconFilepaths(replacementParentPath: str = None):
def getIconFilepaths():
	icons = {}
	iconFiles = [f for f in iconsFolder.iterdir() if (iconsFolder / f).is_file()]
	for filePath in iconFiles:
		iconName = filePath.stem
		#if replacementParentPath:
		#	filePath = Path(replacementParentPath) / filePath.relative_to(pathHere)
		icons[iconName] = filePath
	return icons

def getIconImages():
	iconFilepaths = getIconFilepaths()
	icons = {}
	for iconName,filePath in iconFilepaths.items():
		icons[iconName] = Image.open(filePath, 'r')
	return icons

def getGraphicsFilepath(filename):
	return str(graphicsFolder / filename)

def openGraphicsImage(imgFilename):
	filePath = getGraphicsFilepath(imgFilename)
	return Image.open(filePath, 'r')