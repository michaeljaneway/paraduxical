class Coordinate:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def equals(self, coord: "Coordinate") -> bool:
        return coord.x == self.x and coord.y == self.y

    def isAdjacent(self, coord: "Coordinate") -> bool:
        raise NotImplementedError