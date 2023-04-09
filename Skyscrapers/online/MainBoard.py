import sys
from pathlib import Path
pathHere = Path(__file__).absolute().parent
sys.path.append(str(pathHere.parent))
sys.path.append(str(pathHere.parent.parent))

from tsobg import UIInterface
import board_data

tileGraphicsFolder = "graphics"
floorGraphicsFolder = "graphics"

class MainBoard():


    tileSize = 100 # tile size in pixels
    lotSize = 80 # lot size in pixels
    floorShiftX = 10
    floorShiftY = -20

    
    def _getDivID(tileX, tileY, i):
        return "floor_" + str(tileX) + "_" + str(tileY) + "_" + str(i)

    def _getFloorFilename(floor):
        return "game_file/" + floorGraphicsFolder + "/" + "floor_" + floor + ".png"

    def getCityAreaUISize(self):
        return (self.getNColumns() * MainBoard.tileSize, self.getNRows() * MainBoard.tileSize)

    def _getFloorImgUIPos(self, tileX, tileY, i):
        # Using css coordinate system (origo is in top left)
        tileSize = MainBoard.tileSize
        lotSize = MainBoard.lotSize
        lotOffset = (tileSize - lotSize) / 2  # tile to lot offset
        tileTopLeftCorner = (tileX * tileSize, tileY * tileSize)
        lotTopLeftCorner = (tileTopLeftCorner[0] + lotOffset, tileTopLeftCorner[1] + lotOffset)
        floorImgTopLeftCorner = (lotTopLeftCorner[0] + MainBoard.floorShiftX * i, lotTopLeftCorner[1] + MainBoard.floorShiftY * (i + 1))
        return floorImgTopLeftCorner

    def _initGrid(self, map):
        self.grid = [list(row) for row in board_data.map]

    def __init__(self, uiInterface: UIInterface):
        self.uiInterface = uiInterface
        self._initGrid(board_data.map)
        uiInterface.stageUIChange(("set_div", "main_board", {"parent": "center", "size": (1000, 700), "img":"game_file/generated_graphics/map.png"}))

    def getNRows(self):
        return len(self.grid)

    def getNColumns(self):
        return len(self.grid[0])
    
    def getTileType(self, tileX, tileY):
        """ returns Possible values: WATER/GREEN/PARKING/LOT string char for unbuilt, or a list of floors for building"""
        tile = self.grid[tileY][tileX]
        return board_data.LOT if isinstance(tile, list) else tile

    def isLot(self, tileX, tileY):
        tile = self.grid[tileY][tileX]
        return tile == board_data.LOT or isinstance(tile, list)

    def isEmptyLot(self, tileX, tileY):
        tile = self.grid[tileY][tileX]
        return tile == board_data.LOT

    def isBuiltLot(self, tileX, tileY):
        tile = self.grid[tileY][tileX]
        return isinstance(tile, list) and len(tile) > 0

    def getFloors(self, tileX, tileY):
        """ returns None if not a lot, returns [] if empty lot, and list if floors if built lot """
        tile = self.grid[tileY][tileX]
        if isinstance(tile, list):
            # make copy so we later can compare old with new building
            return tile.copy()
        elif tile == board_data.LOT:
            return []
        else:
            return None

    def setFloors(self, tileX, tileY, floors):
        assert(self.isLot(tileX, tileY))
        
        oldFloors = self.getFloors(tileX, tileY)
        oldHeight = len(oldFloors)
        newHeight = len(floors)
        
        for i in range(0,oldHeight):
            divID = MainBoard._getDivID(tileX, tileY, i)
            if i >= newHeight:
                # remove floor
                self.uiInterface.stageUIChange(("set_div", divID, {"parent":None}))
            elif oldFloors[i] != floors[i]:
                # change floor image
                filename = MainBoard._getFloorFilename(floors[i])
                self.uiInterface.stageUIChange(("set_div", divID, {"img":filename}))
        
        for i in range(oldHeight, newHeight):
            # add floor
            divID = MainBoard._getDivID(tileX, tileY, i)
            filename = MainBoard._getFloorFilename(floors[i])
            uiPos = self._getFloorImgUIPos(tileX, tileY, i)
            divOpts = {"parent":"main_board", "divPositioning":"absolute", "img":filename, "pos":uiPos}
            self.uiInterface.stageUIChange(("set_div", divID, divOpts))
        
        self.grid[tileY][tileX] = floors.copy()


    

        


