from Coordinate import Coordinate


class Token:
    def __init__(self) -> None:
        self.color: str = ""
        self.position: Coordinate

    def getPosition(self) -> Coordinate:
        return self.position

    def setPosition(self, coord: Coordinate) -> None:
        self.position = coord
