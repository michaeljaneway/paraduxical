from enum import  StrEnum


class MoveType(StrEnum):
    """Movement types that can be made in Paradux"""

    NULL = "Null"
    """Empty MoveType"""

    SWAP = "Swap"
    """Swaps two adjacent tokens of opposite color"""

    SHIFT = "Shift"
    """Shift two adjacent tokens in a single direction"""

    def is_valid_movetype(self):
        return self in (MoveType.SWAP, MoveType.SHIFT)
