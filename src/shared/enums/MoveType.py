from enum import IntEnum


class MoveType(IntEnum):
    """Movement types that can be made in Paradux"""

    NULL = 0
    """Empty MoveType"""

    SWAP = 1
    """Swaps two adjacent tokens of opposite color"""

    SHIFT = 2
    """Shift two adjacent tokens in a single direction"""

    def is_valid_movetype(self):
        return self in (MoveType.SWAP, MoveType.SHIFT)
