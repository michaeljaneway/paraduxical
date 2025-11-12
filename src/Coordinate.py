from dataclasses import dataclass
from typing import ClassVar

from enums import Direction


@dataclass(frozen=True)
class Coordinate:
    """A 3D coordinate on a hexagonal board"""

    q: int
    r: int
    s: int

    direction_map: ClassVar[dict[Direction, tuple[int, int, int]]] = {
        Direction.NoDirection: (0, 0, 0),
        Direction.NE: (1, -1, 0),
        Direction.E: (1, 0, -1),
        Direction.SE: (0, 1, -1),
        Direction.SW: (-1, 1, 0),
        Direction.W: (-1, 0, 1),
        Direction.NW: (0, -1, 1),
    }

    def __add__(self, other: "Coordinate | int") -> "Coordinate":
        """Addition overload, supports: Coordinates, int"""
        if isinstance(other, Coordinate):
            return Coordinate(self.q + other.q, self.r + other.r, self.s + other.s)
        return Coordinate(self.q + other, self.r + other, self.s + other)

    def __sub__(self, other: "Coordinate | int ") -> "Coordinate":
        """Subtraction overload, supports: Coordinates, int"""
        if isinstance(other, Coordinate):
            return Coordinate(self.q - other.q, self.r - other.r, self.s - other.s)
        return Coordinate(self.q - other, self.r - other, self.s - other)

    def __mul__(self, other: "Coordinate | int") -> "Coordinate":
        """Mult overload, supports: Coordinates, int"""
        if isinstance(other, Coordinate):
            return Coordinate(self.q * other.q, self.r * other.r, self.s * other.s)
        return Coordinate(self.q * other, self.r * other, self.s * other)

    def __str__(self) -> str:
        return f"(q: {self.q}, r: {self.r}, s: {self.s})"

    def neighbor(self, direction: Direction) -> "Coordinate":
        """Returns the direct neighbor coordinate in the given direction"""
        return self + Coordinate(*self.direction_map[direction])

    def distance(self, other: "Coordinate") -> int:
        """Returns the distance between two coordinates"""
        vec = self - other
        return (abs(vec.q) + abs(vec.r) + abs(vec.s)) // 2

    def ring(self, radius: int) -> list["Coordinate"]:
        """Returns a list of coordinates which form a ring of given radius around the Coordinate"""
        if radius <= 0:
            raise ValueError("Radius must be > 0")

        results: list[Coordinate] = []
        hex = self + Coordinate(*self.direction_map[Direction.SW]) * radius
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
        """Returns a list of coordinates which form a spiral of given radius around the Coordinate"""
        results = [Coordinate(self.q, self.r, self.s)]
        for k in range(1, radius + 1):
            results += self.ring(k)
        return results
