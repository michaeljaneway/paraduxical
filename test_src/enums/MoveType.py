from enum import Enum


class MoveType(Enum):
    """Enum representing the possible movement types that can be made"""

    SWAP = 0
    """Swaps two adjacent tokens of opposite color"""

    SHIFT = 1
    """Shift two adjacent tokens in a single direction"""
