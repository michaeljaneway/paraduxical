from dataclasses import dataclass
from enum import Enum
from enums.TokenType import TokenType



class Direction(Enum):
    NoDirection = (0, 0, 0)
    NE = (1, -1, 0)
    E = (1, 0, -1)
    SE = (0, 1, -1)
    SW = (-1, 1, 0)
    W = (-1, 0, 1)
    NW = (0, -1, 1)


@dataclass(frozen=True)
class Cube:
    q: int
    r: int
    s: int

    def add(self, vec: tuple[int, int, int]) -> 'Cube':
        return Cube(self.q + vec[0], self.r + vec[1], self.s + vec[2])

    def scale(self, factor: int) -> 'Cube':
        return Cube(self.q * factor, self.r * factor, self.s * factor)

    def neighbor(self, direction: Direction) -> 'Cube':
        return self.add(direction.value)

    def to_tuple(self) -> tuple[int, int, int]:
        return (self.q, self.r, self.s)

    @staticmethod
    def direction(direction: Direction) -> 'Cube':
        return Cube(direction.value[0], direction.value[1], direction.value[2])

    @staticmethod
    def ring(center: 'Cube', radius: int) -> list['Cube']:
        if radius <= 0:
            raise ValueError("Radius must be > 0")

        results: list[Cube] = []
        hex = center.add(center.direction(Direction.SW).scale(radius).to_tuple())

        ring_order = [
            Direction.E, Direction.NE, Direction.NW, Direction.W, Direction.SW, Direction.SE
        ]

        for dir in ring_order:
            for _ in range(radius):
                results.append(hex)
                hex = hex.neighbor(dir)

        return results

    @staticmethod
    def spiral(center: 'Cube', radius: int) -> list['Cube']:
        results = [center]
        for k in range(1, radius+1):
            results += Cube.ring(center, k)
        return results


class Board:
    """
    Represents a hexagonal game board with a given radius
    Uses the Cube hexagonal coordinate system: https://www.redblobgames.com/grids/hexagons
    """

    def __init__(self, radius: int = 4) -> None:
        self.radius: int = radius
        self.board_map: dict[Cube, TokenType] =  {val: TokenType.INV for val in Cube.spiral(Cube(0,0,0), radius)}
        
    def index_to_cube(self, x: int, y: int):
        x = (x//2) - (self.radius - 1)
        y = y - (self.radius - 1)
        
        print(x, y)


class Game():
    pass

if __name__ == '__main__':
    b = Board(3)
    print(b.board_map)
    
    x = (ord('F'.lower()) - 97) // 2
    y = int(3) - 1
    
    b.index_to_cube(x, y)
    

