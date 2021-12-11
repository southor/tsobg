from PIL import Image
from pathlib import Path

pathHere = Path(__file__).absolute().parent

iconsFolder = pathHere / "icons"
graphicsFolder = pathHere / "graphics"


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

def getGrapchisFilepath(filename):
	return str(graphicsFolder / filename)