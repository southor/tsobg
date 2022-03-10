from PIL import Image

import graphics
import card_graphics
import board_data


def makeBoardImage():
	tileImages = {}
	tileImages[board_data.PARKING] = graphics.openGraphicsImage("tile_parking.png")
	tileImages[board_data.GREEN] = graphics.openGraphicsImage("tile_green.png")
	tileImages[board_data.WATER] = graphics.openGraphicsImage("tile_water.png")
	tileImages[board_data.LOT] = graphics.openGraphicsImage("tile_lot.png")
	tileSize = tileImages[board_data.LOT].size
	nTilesY = len(board_data.map)
	nTilesX = len(board_data.map[0])
	board = Image.new('RGBA', (nTilesX * tileSize[0], nTilesY * tileSize[1]), (255, 255, 255, 255))
	for tileX in range(0, nTilesX):
		for tileY in range(0, nTilesY):
			tileType = board_data.map[tileY][tileX]
			img = tileImages[tileType]
			offset = (tileX*tileSize[0], tileY*tileSize[1])
			board.paste(img, offset)
	graphics.graphicsOutputFolder.mkdir(exist_ok=True)
	filePath = graphics.graphicsOutputFolder / "map.png"
	board.save(str(filePath))


if __name__ == "__main__":
	print("generating board...")
	makeBoardImage()
	print("generating cards...")
	card_graphics.makeAllCardImages()
	print("done")

