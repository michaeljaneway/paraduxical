class Position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Position):
            return False
        return self.x == value.x and self.y == value.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
