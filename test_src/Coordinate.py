from dataclasses import dataclass
from enums.Direction import Direction

direction_map = {
    Direction.NoDirection: (0, 0, 0),
    Direction.NE: (1, -1, 0),
    Direction.E: (1, 0, -1),
    Direction.SE: (0, 1, -1),
    Direction.SW: (-1, 1, 0),
    Direction.W: (-1, 0, 1),
    Direction.NW: (0, -1, 1),
}


@dataclass(frozen=True)
class Coordinate:
    q: int
    r: int
    s: int

    def __add__(self, other: "Coordinate | int") -> "Coordinate":
        if isinstance(other, Coordinate):
            return Coordinate(self.q + other.q, self.r + other.r, self.s + other.s)
        return Coordinate(self.q + other, self.r + other, self.s + other)

    def __sub__(self, other: "Coordinate | int ") -> "Coordinate":
        if isinstance(other, Coordinate):
            return Coordinate(self.q - other.q, self.r - other.r, self.s - other.s)
        return Coordinate(self.q - other, self.r - other, self.s - other)

    def __mul__(self, other: "Coordinate | int") -> "Coordinate":
        if isinstance(other, Coordinate):
            return Coordinate(self.q * other.q, self.r * other.r, self.s * other.s)
        return Coordinate(self.q * other, self.r * other, self.s * other)

    def neighbor(self, direction: Direction) -> "Coordinate":
        return self + Coordinate(*direction_map[direction])

    def ring(self, radius: int) -> list["Coordinate"]:
        if radius <= 0:
            raise ValueError("Radius must be > 0")

        results: list[Coordinate] = []
        hex = self + Coordinate(*direction_map[Direction.SW]) * radius
        ring_order = [
            Direction.E,
            Direction.NE,
            Direction.NW,
            Direction.W,
            Direction.SW,
            Direction.SE,
        ]

        for dir in ring_order:
            for _ in range(radius):
                results.append(hex)
                hex = hex.neighbor(dir)
        return results

    def spiral(self, radius: int) -> list["Coordinate"]:
        results = [Coordinate(self.q, self.r, self.s)]
        for k in range(1, radius + 1):
            results += self.ring(k)
        return results
